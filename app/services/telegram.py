import asyncio
import secrets
from dataclasses import dataclass
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.models import TelegramUser, User
from app.services.conversations import send_chat_message


class TelegramConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class TelegramMessage:
    update_id: int
    chat_id: int
    user_id: int
    text: str


def get_telegram_token() -> str:
    token = get_settings().telegram_bot_token
    if not token:
        raise TelegramConfigError("TELEGRAM_BOT_TOKEN is required")
    return token


def parse_allowed_user_ids(value: str | None = None) -> set[int]:
    raw = get_settings().telegram_allowed_user_ids if value is None else value
    if not raw:
        return set()
    allowed: set[int] = set()
    for item in raw.split(","):
        item = item.strip()
        if item:
            allowed.add(int(item))
    return allowed


def is_allowed_user(user_id: int, allowed_ids: set[int] | None = None) -> bool:
    allowed = parse_allowed_user_ids() if allowed_ids is None else allowed_ids
    return not allowed or user_id in allowed


def parse_update(update: dict[str, Any]) -> TelegramMessage | None:
    message = update.get("message")
    if not isinstance(message, dict):
        return None
    text = message.get("text")
    chat = message.get("chat")
    user = message.get("from")
    if not isinstance(text, str) or not isinstance(chat, dict) or not isinstance(user, dict):
        return None
    chat_id = chat.get("id")
    user_id = user.get("id")
    update_id = update.get("update_id")
    if not isinstance(chat_id, int) or not isinstance(user_id, int) or not isinstance(update_id, int):
        return None
    return TelegramMessage(
        update_id=update_id,
        chat_id=chat_id,
        user_id=user_id,
        text=text.strip(),
    )


def get_or_create_telegram_user(
    db: Session,
    telegram_user_id: int,
    telegram_chat_id: int,
) -> TelegramUser:
    mapping = db.scalar(
        select(TelegramUser).where(TelegramUser.telegram_user_id == telegram_user_id)
    )
    if mapping:
        if mapping.telegram_chat_id != telegram_chat_id:
            mapping.telegram_chat_id = telegram_chat_id
            db.commit()
            db.refresh(mapping)
        return mapping

    username = f"telegram_{telegram_user_id}"
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        user = User(
            username=username,
            password_hash=hash_password(secrets.token_urlsafe(32)),
        )
        db.add(user)
        db.flush()

    mapping = TelegramUser(
        telegram_user_id=telegram_user_id,
        telegram_chat_id=telegram_chat_id,
        user_id=user.id,
    )
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return mapping


def handle_start_message() -> str:
    return "Hi. Send me a message and I will reply using the chatbot."


def handle_text_message(db: Session, message: TelegramMessage) -> str:
    mapping = get_or_create_telegram_user(
        db,
        telegram_user_id=message.user_id,
        telegram_chat_id=message.chat_id,
    )
    user = db.get(User, mapping.user_id)
    if user is None:
        raise RuntimeError("Mapped Telegram user is missing")

    conversation, assistant_message = send_chat_message(
        db,
        user,
        message.text,
        mapping.conversation_id,
    )
    if mapping.conversation_id is None:
        mapping.conversation_id = conversation.id
        db.commit()
    return assistant_message.content


def handle_telegram_message(
    db: Session,
    message: TelegramMessage,
    allowed_ids: set[int] | None = None,
) -> str:
    if not is_allowed_user(message.user_id, allowed_ids):
        return "Not authorized."
    if message.text == "/start":
        get_or_create_telegram_user(db, message.user_id, message.chat_id)
        return handle_start_message()
    return handle_text_message(db, message)


class TelegramClient:
    def __init__(self, token: str):
        self.base_url = f"https://api.telegram.org/bot{token}"

    async def get_updates(self, offset: int | None = None, timeout: int = 30) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"timeout": timeout, "allowed_updates": ["message"]}
        if offset is not None:
            params["offset"] = offset
        async with httpx.AsyncClient(timeout=timeout + 10) as client:
            response = await client.get(f"{self.base_url}/getUpdates", params=params)
            response.raise_for_status()
            payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError("Telegram getUpdates failed")
        return list(payload.get("result", []))

    async def send_message(self, chat_id: int, text: str) -> None:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            )
            response.raise_for_status()


async def poll_telegram(client: TelegramClient, db_factory, delay_seconds: float = 1.0) -> None:
    offset: int | None = None
    while True:
        updates = await client.get_updates(offset=offset)
        for update in updates:
            offset = int(update["update_id"]) + 1
            message = parse_update(update)
            if message is None:
                continue
            with db_factory() as db:
                reply = handle_telegram_message(db, message)
            await client.send_message(message.chat_id, reply)
        await asyncio.sleep(delay_seconds)
