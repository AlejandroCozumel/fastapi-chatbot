from unittest.mock import patch

import pytest

from app.core.config import get_settings
from app.db.models import Message, TelegramUser, User
from app.services.telegram import (
    TelegramConfigError,
    TelegramMessage,
    get_or_create_telegram_user,
    get_telegram_token,
    handle_telegram_message,
    parse_update,
)


def test_telegram_user_mapping_creation_and_reuse(db_session):
    first = get_or_create_telegram_user(db_session, 123, 999)
    second = get_or_create_telegram_user(db_session, 123, 999)

    assert first.id == second.id
    assert first.user_id == second.user_id
    assert db_session.get(User, first.user_id).username == "telegram_123"


def test_allowed_user_filtering(db_session):
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="hello")

    reply = handle_telegram_message(db_session, message, allowed_ids={456})

    assert reply == "Not authorized."
    assert db_session.query(TelegramUser).count() == 0


def test_start_response_creates_mapping(db_session):
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="/start")

    reply = handle_telegram_message(db_session, message, allowed_ids={123})

    assert "Send me a message" in reply
    assert db_session.query(TelegramUser).count() == 1


def test_text_message_routes_into_existing_chat_logic(db_session):
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="hello")

    with patch(
        "app.services.conversations.get_assistant_response",
        return_value="telegram reply",
    ):
        reply = handle_telegram_message(db_session, message, allowed_ids={123})

    mapping = db_session.query(TelegramUser).one()
    messages = db_session.query(Message).order_by(Message.id).all()
    assert reply == "telegram reply"
    assert mapping.conversation_id is not None
    assert [item.role for item in messages] == ["user", "assistant"]


def test_parse_update_ignores_unsupported_update():
    assert parse_update({"update_id": 1, "edited_message": {}}) is None


def test_missing_telegram_token_has_clear_error(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    get_settings.cache_clear()

    with pytest.raises(TelegramConfigError, match="TELEGRAM_BOT_TOKEN is required"):
        get_telegram_token()

    get_settings.cache_clear()
