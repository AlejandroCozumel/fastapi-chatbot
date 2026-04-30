from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Document, DocumentChunk, User
from app.services.rag import create_embedding, serialize_embedding


SUPPORTED_CONTENT_TYPES = {
    "text/plain",
    "text/markdown",
    "application/pdf",
}


def _extract_text(path: Path, content_type: str | None) -> str:
    if content_type == "application/pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def _chunks(text: str, size: int = 1200, overlap: int = 150) -> list[str]:
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(clean):
        chunks.append(clean[start : start + size])
        start += size - overlap
    return chunks


def index_document_text(
    db: Session,
    user: User,
    filename: str,
    text: str,
    content_type: str | None = "text/markdown",
    storage_path: str | None = None,
) -> Document:
    document = Document(
        user_id=user.id,
        filename=filename,
        content_type=content_type,
        storage_path=storage_path or filename,
        status="uploaded",
    )
    db.add(document)
    db.flush()

    chunk_texts = _chunks(text)
    if not chunk_texts:
        document.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document has no extractable text",
        )

    for index, content in enumerate(chunk_texts):
        embedding = create_embedding(content)
        db.add(
            DocumentChunk(
                document_id=document.id,
                user_id=user.id,
                chunk_index=index,
                content=content,
                embedding_json=serialize_embedding(embedding),
            )
        )
    document.status = "processed"
    db.commit()
    db.refresh(document)
    return document


async def upload_document(db: Session, user: User, file: UploadFile) -> Document:
    settings = get_settings()
    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported document type",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large",
        )

    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid4().hex}_{Path(file.filename or 'upload.txt').name}"
    path = settings.upload_dir / safe_name
    path.write_bytes(data)

    document = Document(
        user_id=user.id,
        filename=file.filename or safe_name,
        content_type=file.content_type,
        storage_path=str(path),
        status="uploaded",
    )
    db.add(document)
    db.flush()

    try:
        text = _extract_text(path, file.content_type)
        db.delete(document)
        db.flush()
        return index_document_text(
            db,
            user,
            filename=file.filename or safe_name,
            text=text,
            content_type=file.content_type,
            storage_path=str(path),
        )
    except HTTPException:
        raise
    except Exception as exc:
        document.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing failed",
        ) from exc
