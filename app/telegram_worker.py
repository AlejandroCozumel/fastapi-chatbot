import asyncio

from app.db.session import SessionLocal, init_db
from app.services.telegram import TelegramClient, get_telegram_token, poll_telegram


def main() -> None:
    init_db()
    token = get_telegram_token()
    client = TelegramClient(token)
    asyncio.run(poll_telegram(client, SessionLocal))


if __name__ == "__main__":
    main()
