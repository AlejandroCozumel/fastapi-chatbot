from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmailDraftRequest(BaseModel):
    recipient: EmailStr
    subject: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)


class EmailDraftResponse(BaseModel):
    id: int
    recipient: str
    subject: str
    body: str
    status: str
    created_at: datetime
    confirmed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ConfirmEmailRequest(BaseModel):
    confirm: bool
    recipient: EmailStr
    subject: str
    body: str


class EmailSendResponse(BaseModel):
    draft_id: int
    status: str
    provider_message_id: str | None = None
    error_message: str | None = None
