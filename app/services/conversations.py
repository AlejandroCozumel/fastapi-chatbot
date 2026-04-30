from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Conversation, Message, User, utcnow
from app.services.chat import get_assistant_response


def _title_from_message(message: str) -> str:
    title = message.strip().splitlines()[0][:80]
    return title or "New conversation"


def get_user_conversation(
    db: Session,
    user: User,
    conversation_id: int,
) -> Conversation:
    conversation = db.scalar(
        select(Conversation)
        .where(Conversation.id == conversation_id, Conversation.user_id == user.id)
        .options(selectinload(Conversation.messages))
    )
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation


def list_conversations(db: Session, user: User) -> list[Conversation]:
    return list(
        db.scalars(
            select(Conversation)
            .where(Conversation.user_id == user.id)
            .order_by(Conversation.updated_at.desc())
        )
    )


def send_chat_message(
    db: Session,
    user: User,
    message: str,
    conversation_id: int | None = None,
) -> tuple[Conversation, Message]:
    assistant_content = get_assistant_response(message)
    return save_chat_exchange(db, user, message, assistant_content, conversation_id)


def save_chat_exchange(
    db: Session,
    user: User,
    message: str,
    assistant_content: str,
    conversation_id: int | None = None,
) -> tuple[Conversation, Message]:
    if conversation_id is None:
        conversation = Conversation(user_id=user.id, title=_title_from_message(message))
        db.add(conversation)
        db.flush()
    else:
        conversation = get_user_conversation(db, user, conversation_id)

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )
    db.add(user_message)
    db.flush()

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_content,
    )
    conversation.updated_at = utcnow()
    db.add(assistant_message)
    db.commit()
    db.refresh(conversation)
    db.refresh(assistant_message)
    return conversation, assistant_message
