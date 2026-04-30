from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentQueryRequest(BaseModel):
    question: str = Field(min_length=1)


class DocumentQueryResponse(BaseModel):
    answer: str
    document_ids: list[int]
    context: str
