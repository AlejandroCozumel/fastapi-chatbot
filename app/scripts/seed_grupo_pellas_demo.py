import argparse

from sqlalchemy import select

from app.db.models import TelegramUser, User
from app.db.session import SessionLocal, init_db
from app.services.demo_documents import seed_demo_documents_for_user
from app.services.telegram import get_or_create_telegram_user, parse_allowed_user_ids


def seed_documents(telegram_user_id: int, telegram_chat_id: int | None = None) -> int:
    init_db()
    chat_id = telegram_chat_id or telegram_user_id
    with SessionLocal() as db:
        mapping = get_or_create_telegram_user(
            db,
            telegram_user_id,
            chat_id,
            auto_seed_demo_documents=False,
        )
        user = db.get(User, mapping.user_id)
        if user is None:
            raise RuntimeError("Mapped Telegram user is missing")

        return seed_demo_documents_for_user(db, user)


def get_known_telegram_user_ids() -> list[int]:
    init_db()
    with SessionLocal() as db:
        return list(
            db.scalars(
                select(TelegramUser.telegram_user_id).order_by(
                    TelegramUser.telegram_user_id
                )
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed Grupo Pellas demo documents for a Telegram user."
    )
    parser.add_argument(
        "--telegram-user-id",
        type=int,
        help="Telegram user id. Defaults to TELEGRAM_ALLOWED_USER_IDS when omitted.",
    )
    parser.add_argument("--telegram-chat-id", type=int)
    args = parser.parse_args()

    telegram_user_ids = (
        [args.telegram_user_id]
        if args.telegram_user_id is not None
        else sorted(parse_allowed_user_ids())
    )
    if not telegram_user_ids:
        telegram_user_ids = get_known_telegram_user_ids()
    if not telegram_user_ids:
        parser.error(
            "no Telegram user found. Set TELEGRAM_ALLOWED_USER_IDS, pass "
            "--telegram-user-id, or message the bot once before seeding."
        )
    if args.telegram_chat_id is not None and len(telegram_user_ids) != 1:
        parser.error("--telegram-chat-id can only be used with one Telegram user id")

    count = 0
    for telegram_user_id in telegram_user_ids:
        count += seed_documents(telegram_user_id, args.telegram_chat_id)
    print(
        f"Seeded {count} Grupo Pellas demo documents "
        f"for {len(telegram_user_ids)} Telegram user(s)."
    )


if __name__ == "__main__":
    main()
