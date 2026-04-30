import asyncio
import html
import re
import secrets
from dataclasses import dataclass
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import TypeAdapter, ValidationError
from pydantic.networks import EmailStr

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.models import Message, TelegramUser, User
from app.schemas.email import ConfirmEmailRequest, EmailDraftRequest
from app.services.chat import get_assistant_response
from app.services.conversations import save_chat_exchange, send_chat_message
from app.services.demo_documents import seed_demo_documents_for_user
from app.services.email import confirm_and_send_email, create_email_draft
from app.services.rag import answer_from_documents, user_has_document_chunks


class TelegramConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class TelegramMessage:
    update_id: int
    chat_id: int
    user_id: int
    text: str


PENDING_EMAIL_SENDS: set[int] = set()
EMAIL_ADAPTER = TypeAdapter(EmailStr)


def format_telegram_html(text: str) -> str:
    formatted_lines: list[str] = []
    for line in text.splitlines():
        formatted_lines.append(re.sub(r"^#{1,6}\s*", "", line))

    escaped = html.escape("\n".join(formatted_lines), quote=False)
    return re.sub(r"\*\*([^*\n]+)\*\*", r"<b>\1</b>", escaped)


def format_email_html(text: str) -> str:
    blocks: list[str] = []
    bullet_items: list[str] = []

    def flush_bullets() -> None:
        if bullet_items:
            blocks.append("<ul>" + "".join(bullet_items) + "</ul>")
            bullet_items.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            flush_bullets()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            flush_bullets()
            level = min(len(heading_match.group(1)) + 1, 4)
            content = _format_inline_email_html(heading_match.group(2))
            blocks.append(f"<h{level}>{content}</h{level}>")
            continue

        bullet_match = re.match(r"^[-*]\s+(.+)$", line)
        if bullet_match:
            bullet_items.append(f"<li>{_format_inline_email_html(bullet_match.group(1))}</li>")
            continue

        flush_bullets()
        blocks.append(f"<p>{_format_inline_email_html(line)}</p>")

    flush_bullets()
    return "\n".join(blocks)


def _format_inline_email_html(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", escaped)


def validate_recipient_email(value: str) -> str | None:
    try:
        return str(EMAIL_ADAPTER.validate_python(value.strip()))
    except ValidationError:
        return None


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
    auto_seed_demo_documents: bool = True,
) -> TelegramUser:
    mapping = db.scalar(
        select(TelegramUser).where(TelegramUser.telegram_user_id == telegram_user_id)
    )
    if mapping:
        if mapping.telegram_chat_id != telegram_chat_id:
            mapping.telegram_chat_id = telegram_chat_id
            db.commit()
            db.refresh(mapping)
        if auto_seed_demo_documents:
            user = db.get(User, mapping.user_id)
            if user is None:
                raise RuntimeError("Mapped Telegram user is missing")
            seed_demo_documents_for_user(db, user)
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
    if auto_seed_demo_documents:
        seed_demo_documents_for_user(db, user)
    return mapping


def handle_start_message() -> str:
    return (
        "Hi. Send me a message and I will reply using the chatbot. "
        "If demo documents are loaded for your Telegram user, I can answer using them. "
        "Send /send when you want me to email your profile summary."
    )


def build_profile_email_body(db: Session, user: User) -> str:
    messages = list(
        db.scalars(
            select(Message)
            .join(Message.conversation)
            .where(Message.conversation.has(user_id=user.id))
            .order_by(Message.created_at.desc())
            .limit(20)
        )
    )
    messages.reverse()
    transcript = "\n".join(
        f"{message.role}: {message.content}" for message in messages
    )
    if not transcript:
        transcript = "No previous chat messages are available for this Telegram user."

    prompt = (
        "Create a concise customer profile summary from this Telegram chatbot "
        "conversation. Include likely interests, requested products, questions, "
        "and next steps. Do not invent personal data.\n\n"
        f"Conversation:\n{transcript}"
    )
    summary = get_assistant_response(prompt)
    return (
        "<h1>Telegram customer profile</h1>"
        f"{format_email_html(summary)}"
    )


def send_profile_email(db: Session, user: User, recipient: str) -> str:
    body = build_profile_email_body(db, user)
    draft = create_email_draft(
        db,
        user,
        EmailDraftRequest(
            recipient=recipient,
            subject="Telegram customer profile",
            body=body,
        ),
    )
    record = confirm_and_send_email(
        db,
        user,
        draft.id,
        ConfirmEmailRequest(
            confirm=True,
            recipient=draft.recipient,
            subject=draft.subject,
            body=draft.body,
        ),
    )
    if record.status != "sent":
        return f"Email send failed: {record.error_message or 'unknown error'}"
    return f"Email sent to {recipient}."


def handle_send_command(message: TelegramMessage) -> str:
    PENDING_EMAIL_SENDS.add(message.user_id)
    return "Send me the email address where I should send your profile summary."


def handle_pending_email_send(db: Session, message: TelegramMessage, user: User) -> str:
    recipient = validate_recipient_email(message.text)
    if recipient is None:
        return "That does not look like a valid email address. Send a valid email or /cancel."
    PENDING_EMAIL_SENDS.discard(message.user_id)
    return send_profile_email(db, user, recipient)


def handle_text_message(db: Session, message: TelegramMessage) -> str:
    mapping = get_or_create_telegram_user(
        db,
        telegram_user_id=message.user_id,
        telegram_chat_id=message.chat_id,
    )
    user = db.get(User, mapping.user_id)
    if user is None:
        raise RuntimeError("Mapped Telegram user is missing")

    if message.text == "/cancel":
        PENDING_EMAIL_SENDS.discard(message.user_id)
        return "Cancelled."
    if message.text == "/send":
        return handle_send_command(message)
    if message.user_id in PENDING_EMAIL_SENDS:
        return handle_pending_email_send(db, message, user)

    if user_has_document_chunks(db, user):
        assistant_content, _, _ = answer_from_documents(db, user, message.text)
        conversation, assistant_message = save_chat_exchange(
            db,
            user,
            message.text,
            assistant_content,
            mapping.conversation_id,
        )
    else:
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
                json={
                    "chat_id": chat_id,
                    "text": format_telegram_html(text),
                    "parse_mode": "HTML",
                },
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
