from typing import Any

import resend
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import EmailDraft, EmailSendRecord, User, utcnow
from app.schemas.email import ConfirmEmailRequest, EmailDraftRequest


def create_email_draft(db: Session, user: User, payload: EmailDraftRequest) -> EmailDraft:
    draft = EmailDraft(
        user_id=user.id,
        recipient=str(payload.recipient),
        subject=payload.subject,
        body=payload.body,
        status="draft",
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


def _get_user_draft(db: Session, user: User, draft_id: int) -> EmailDraft:
    draft = db.get(EmailDraft, draft_id)
    if draft is None or draft.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email draft not found",
        )
    return draft


def _validate_confirmation(draft: EmailDraft, payload: ConfirmEmailRequest) -> None:
    if not payload.confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Explicit confirmation is required",
        )
    if (
        draft.recipient != str(payload.recipient)
        or draft.subject != payload.subject
        or draft.body != payload.body
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Confirmation does not match draft",
        )


def _send_with_resend(draft: EmailDraft) -> str:
    settings = get_settings()
    if not settings.resend_api_key or not settings.resend_from_email:
        return "mock-resend-message-id"

    resend.api_key = settings.resend_api_key
    response: Any = resend.Emails.send(
        {
            "from": settings.resend_from_email,
            "to": [draft.recipient],
            "subject": draft.subject,
            "html": draft.body,
        }
    )
    if isinstance(response, dict):
        message_id = response.get("id")
    else:
        message_id = getattr(response, "id", None)
    if not message_id:
        raise RuntimeError("Resend did not return a message id")
    return str(message_id)


def confirm_and_send_email(
    db: Session,
    user: User,
    draft_id: int,
    payload: ConfirmEmailRequest,
) -> EmailSendRecord:
    draft = _get_user_draft(db, user, draft_id)
    _validate_confirmation(draft, payload)
    draft.status = "confirmed"
    draft.confirmed_at = utcnow()
    db.flush()

    try:
        provider_message_id = _send_with_resend(draft)
    except Exception as exc:
        draft.status = "failed"
        record = EmailSendRecord(
            draft_id=draft.id,
            user_id=user.id,
            status="failed",
            error_message=str(exc),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    draft.status = "sent"
    record = EmailSendRecord(
        draft_id=draft.id,
        user_id=user.id,
        provider_message_id=provider_message_id,
        status="sent",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
