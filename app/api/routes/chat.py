from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, get_current_user
from app.db.models import User
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationDetail,
    ConversationSummary,
    MessageResponse,
)
from app.services.conversations import (
    get_user_conversation,
    list_conversations,
    send_chat_message,
)


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ChatResponse:
    conversation, assistant_message = send_chat_message(
        db,
        current_user,
        payload.message,
        payload.conversation_id,
    )
    return ChatResponse(
        conversation_id=conversation.id,
        message=MessageResponse.model_validate(assistant_message),
    )


@router.get("/conversations", response_model=list[ConversationSummary])
def conversations(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list:
    return list_conversations(db, current_user)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def conversation_detail(
    conversation_id: int,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return get_user_conversation(db, current_user, conversation_id)
