from unittest.mock import patch

import pytest

from app.core.config import get_settings
from app.db.models import DocumentChunk, EmailDraft, EmailSendRecord, Message, TelegramUser, User
from app.services.documents import index_document_text
from app.services.telegram import (
    PENDING_EMAIL_SENDS,
    TelegramConfigError,
    TelegramMessage,
    format_email_html,
    format_telegram_html,
    get_or_create_telegram_user,
    get_telegram_token,
    handle_telegram_message,
    parse_update,
)


@pytest.fixture(autouse=True)
def clear_pending_email_sends():
    PENDING_EMAIL_SENDS.clear()
    yield
    PENDING_EMAIL_SENDS.clear()


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
        "app.services.rag.get_assistant_response",
        return_value="telegram reply",
    ):
        reply = handle_telegram_message(db_session, message, allowed_ids={123})

    mapping = db_session.query(TelegramUser).one()
    messages = db_session.query(Message).order_by(Message.id).all()
    assert reply == "telegram reply"
    assert mapping.conversation_id is not None
    assert [item.role for item in messages] == ["user", "assistant"]


def test_text_message_uses_documents_when_available(db_session):
    message = TelegramMessage(
        update_id=1,
        chat_id=999,
        user_id=123,
        text="What is the demo warranty?",
    )
    mapping = get_or_create_telegram_user(db_session, 123, 999)
    user = db_session.get(User, mapping.user_id)
    index_document_text(
        db_session,
        user,
        filename="demo.md",
        text="The Grupo Pellas demo vehicle warranty is 12 months.",
    )

    with patch(
        "app.services.rag.get_assistant_response",
        return_value="The demo warranty is 12 months.",
    ):
        reply = handle_telegram_message(db_session, message, allowed_ids={123})

    messages = db_session.query(Message).order_by(Message.id).all()
    assert reply == "The demo warranty is 12 months."
    assert [item.role for item in messages] == ["user", "assistant"]


def test_send_command_asks_for_email_address(db_session):
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="/send")

    reply = handle_telegram_message(db_session, message, allowed_ids={123})

    assert "email address" in reply
    assert 123 in PENDING_EMAIL_SENDS


def test_pending_send_rejects_invalid_email(db_session):
    PENDING_EMAIL_SENDS.add(123)
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="not-email")

    reply = handle_telegram_message(db_session, message, allowed_ids={123})

    assert "valid email" in reply
    assert 123 in PENDING_EMAIL_SENDS


def test_pending_send_emails_profile_summary(db_session):
    PENDING_EMAIL_SENDS.add(123)
    message = TelegramMessage(
        update_id=1,
        chat_id=999,
        user_id=123,
        text="person@example.com",
    )

    with (
        patch(
            "app.services.telegram.get_assistant_response",
            return_value="Customer asked about E-Move financing.",
        ),
        patch("app.services.email._send_with_resend", return_value="msg_telegram"),
    ):
        reply = handle_telegram_message(db_session, message, allowed_ids={123})

    draft = db_session.query(EmailDraft).one()
    record = db_session.query(EmailSendRecord).one()
    assert reply == "Email sent to person@example.com."
    assert 123 not in PENDING_EMAIL_SENDS
    assert draft.recipient == "person@example.com"
    assert draft.subject == "Telegram customer profile"
    assert "Customer asked about E-Move financing." in draft.body
    assert record.status == "sent"
    assert record.provider_message_id == "msg_telegram"


def test_cancel_clears_pending_send(db_session):
    PENDING_EMAIL_SENDS.add(123)
    message = TelegramMessage(update_id=1, chat_id=999, user_id=123, text="/cancel")

    reply = handle_telegram_message(db_session, message, allowed_ids={123})

    assert reply == "Cancelled."
    assert 123 not in PENDING_EMAIL_SENDS


def test_parse_update_ignores_unsupported_update():
    assert parse_update({"update_id": 1, "edited_message": {}}) is None


def test_telegram_formatter_converts_common_markdown_to_html():
    text = "### Modelos de motos:\n- **Electrica E-Move**: USD 35"

    formatted = format_telegram_html(text)

    assert formatted == "Modelos de motos:\n- <b>Electrica E-Move</b>: USD 35"


def test_telegram_formatter_escapes_html_before_formatting():
    text = "### FAQ\n- **Garantia**: <12 meses>"

    formatted = format_telegram_html(text)

    assert formatted == "FAQ\n- <b>Garantia</b>: &lt;12 meses&gt;"


def test_email_formatter_converts_markdown_to_html():
    text = "### Perfil\n- **Interes**: E-Move\n- Pregunto por garantia"

    formatted = format_email_html(text)

    assert formatted == (
        "<h4>Perfil</h4>\n"
        "<ul><li><strong>Interes</strong>: E-Move</li>"
        "<li>Pregunto por garantia</li></ul>"
    )


def test_email_formatter_escapes_html():
    text = "**Nota**: <script>alert('x')</script>"

    formatted = format_email_html(text)

    assert formatted == (
        "<p><strong>Nota</strong>: &lt;script&gt;alert('x')&lt;/script&gt;</p>"
    )


def test_missing_telegram_token_has_clear_error(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    get_settings.cache_clear()

    with pytest.raises(TelegramConfigError, match="TELEGRAM_BOT_TOKEN is required"):
        get_telegram_token()

    get_settings.cache_clear()


def test_grupo_pellas_demo_seed_loads_documents(db_session, tmp_path, monkeypatch):
    from app.services import demo_documents
    from app.scripts import seed_grupo_pellas_demo

    first = tmp_path / "vehicles.md"
    second = tmp_path / "faqs.md"
    first.write_text("Grupo Pellas demo vehicles include Toyota and Suzuki.", encoding="utf-8")
    second.write_text("Demo financing requires ID, income proof, and approval.", encoding="utf-8")
    monkeypatch.setattr(demo_documents, "DEFAULT_DOCUMENTS", (first, second))

    count = seed_grupo_pellas_demo.seed_documents(telegram_user_id=789)

    mapping = db_session.query(TelegramUser).filter_by(telegram_user_id=789).one()
    assert count == 2
    assert db_session.get(User, mapping.user_id).username == "telegram_789"
    assert db_session.query(DocumentChunk).count() == 2


def test_grupo_pellas_demo_seed_is_idempotent(db_session, tmp_path, monkeypatch):
    from app.services import demo_documents
    from app.scripts import seed_grupo_pellas_demo

    document = tmp_path / "vehicles.md"
    document.write_text("Grupo Pellas demo vehicles include Toyota.", encoding="utf-8")
    monkeypatch.setattr(demo_documents, "DEFAULT_DOCUMENTS", (document,))

    first_count = seed_grupo_pellas_demo.seed_documents(telegram_user_id=789)
    second_count = seed_grupo_pellas_demo.seed_documents(telegram_user_id=789)

    assert first_count == 1
    assert second_count == 0
    assert db_session.query(DocumentChunk).count() == 1


def test_grupo_pellas_demo_seed_can_find_known_telegram_users(db_session):
    get_or_create_telegram_user(db_session, 789, 789)

    from app.scripts.seed_grupo_pellas_demo import get_known_telegram_user_ids

    assert get_known_telegram_user_ids() == [789]
