from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, User
from app.services.documents import index_document_text


DEFAULT_DOCUMENTS = (
    Path("sample_documents/grupo_pellas_motos_demo.md"),
    Path("sample_documents/grupo_pellas_vehiculos_faq_demo.md"),
)


def seed_demo_documents_for_user(db: Session, user: User) -> int:
    count = 0
    for path in DEFAULT_DOCUMENTS:
        existing_document_id = db.scalar(
            select(Document.id).where(
                Document.user_id == user.id,
                Document.filename == path.name,
                Document.status == "processed",
            )
        )
        if existing_document_id is not None:
            continue

        text = path.read_text(encoding="utf-8")
        index_document_text(
            db,
            user,
            filename=path.name,
            text=text,
            content_type="text/markdown",
            storage_path=str(path),
        )
        count += 1
    return count
