# Local FastAPI Chatbot Backend

Local-first FastAPI backend for a chatbot with username/password authentication, SQLite persistence, OpenAI chat integration, basic retrieval over uploaded documents, confirmed Resend email sending, and Docker Compose support.

This version intentionally excludes Google OAuth, Gmail, Google Drive, cloud deployment, rate limiting, and advanced logging.

## Requirements

- Python 3.12
- Docker and Docker Compose, optional for container startup
- OpenAI API key for live assistant and embedding calls
- Resend API key and verified sender for live email delivery

Without OpenAI or Resend secrets, the app uses mock-safe behavior for local tests and demos.

## Environment

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Set real values when you want live provider calls:

```text
OPENAI_API_KEY=replace-with-openai-api-key
RESEND_API_KEY=replace-with-resend-api-key
RESEND_FROM_EMAIL=sender@example.com
JWT_SECRET_KEY=change-me-for-local-dev
DATABASE_URL=sqlite:///./data/app.db
UPLOAD_DIR=./data/uploads
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Local Run

```bash
python3 -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Docker Run

```bash
docker compose up --build
```

The app listens on `http://127.0.0.1:8000`.

## Tests

```bash
python3 -m pytest
```

The test suite uses isolated SQLite state and mocks or local fallbacks for external provider behavior.

## API Flow

1. `POST /auth/register`
2. `POST /auth/login`
3. `POST /chat`
4. `GET /conversations`
5. `GET /conversations/{conversation_id}`
6. `POST /documents`
7. `POST /documents/query`
8. `POST /email/drafts`
9. `POST /email/drafts/{draft_id}/send`

Email sends require exact confirmation of recipient, subject, and body before any delivery attempt.
