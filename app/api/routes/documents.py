from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.deps import DbSession, get_current_user
from app.core.errors import AppError, ProviderError
from app.db.models import User
from app.schemas.documents import (
    DocumentQueryRequest,
    DocumentQueryResponse,
    DocumentResponse,
)
from app.services.documents import upload_document
from app.services.rag import answer_from_documents


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=201)
async def upload(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    return await upload_document(db, current_user, file)


@router.post("/query", response_model=DocumentQueryResponse)
def query_documents(
    payload: DocumentQueryRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> DocumentQueryResponse:
    try:
        answer, document_ids, context = answer_from_documents(
            db,
            current_user,
            payload.question,
        )
    except ProviderError as exc:
        if "document context" in exc.message:
            raise AppError(exc.message, status_code=404) from exc
        raise
    return DocumentQueryResponse(
        answer=answer,
        document_ids=document_ids,
        context=context,
    )
