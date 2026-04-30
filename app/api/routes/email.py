from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession, get_current_user
from app.db.models import User
from app.schemas.email import (
    ConfirmEmailRequest,
    EmailDraftRequest,
    EmailDraftResponse,
    EmailSendResponse,
)
from app.services.email import confirm_and_send_email, create_email_draft


router = APIRouter(prefix="/email", tags=["email"])


@router.post(
    "/drafts",
    response_model=EmailDraftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_draft(
    payload: EmailDraftRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return create_email_draft(db, current_user, payload)


@router.post("/drafts/{draft_id}/send", response_model=EmailSendResponse)
def send_draft(
    draft_id: int,
    payload: ConfirmEmailRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> EmailSendResponse:
    record = confirm_and_send_email(db, current_user, draft_id, payload)
    return EmailSendResponse(
        draft_id=record.draft_id,
        status=record.status,
        provider_message_id=record.provider_message_id,
        error_message=record.error_message,
    )
