# Spec Kit Prompts: Local FastAPI Chatbot

Run these prompts from the FastAPI project folder.

## Local Environment

For local development, create a `.env` file from the example:

```bash
cp .env.example .env
```

Generate a local JWT secret:

```bash
openssl rand -hex 32
```

Then set `.env` like this:

```env
OPENAI_API_KEY=your_openai_api_key
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=verified_sender@example.com
JWT_SECRET_KEY=paste_the_generated_secret_here
DATABASE_URL=sqlite:///./data/app.db
UPLOAD_DIR=./data/uploads
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Notes:
- `OPENAI_API_KEY` is only required for real OpenAI chat and embedding calls.
- `RESEND_API_KEY` and `RESEND_FROM_EMAIL` are only required for real email sends.
- `RESEND_FROM_EMAIL` must be a verified sender or domain in Resend.
- Without OpenAI or Resend secrets, the app should keep local mock-safe behavior where possible.

## 1. Create The Spec

```text
/speckit-specify Build a local FastAPI backend for a chatbot with authentication, SQLite storage, OpenAI integration, basic RAG over uploaded documents, Resend email sending, and Docker support.

This is a local-first project, not cloud production. Use SQLite for the database. Use username/password authentication with hashed passwords and JWT access tokens. Do not include Google OAuth, Gmail, Google Drive, cloud deployment, rate limiting, or advanced logging in this version.

The system should allow a user to register, log in, chat with the assistant, store conversation history, upload local documents for retrieval, answer questions using those documents, and send email through Resend only after explicit user confirmation.

Prioritize the implementation in this order:
1. FastAPI base app
2. SQLite database
3. Authentication
4. Basic OpenAI chat
5. Conversation history
6. Document upload
7. RAG search
8. Resend email sending
9. Docker

Include error handling for invalid login, missing token, failed OpenAI calls, missing documents, failed email sends, and malformed requests.

Keep the first version simple and local. Google account integration should be treated as a future feature, not part of this spec.
```

Suggested commit after this step:

```bash
git status
git add specs .specify/feature.json AGENTS.md
git commit -m "spec local FastAPI chatbot backend"
```

## 2. Create The Plan

```text
/speckit-plan Use FastAPI, SQLite, SQLAlchemy or SQLModel, JWT auth, OpenAI Python SDK, Resend API, and Docker Compose. Keep the architecture simple and local-first. The implementation must be divided into milestones that can be implemented and committed separately.
```

Suggested commit after this step:

```bash
git status
git add specs AGENTS.md
git commit -m "plan local FastAPI chatbot backend"
```

## 3. Create The Tasks

```text
/speckit-tasks Divide the implementation into small independent milestones that can each be committed separately. Each milestone should leave the app runnable and testable.

Order the milestones as:
1. Project scaffold and health endpoint
2. SQLite database setup
3. User model and authentication
4. Protected chat endpoint with OpenAI
5. Conversation and message persistence
6. Error handling cleanup
7. Document upload and chunking
8. Embeddings and document search
9. RAG chat integration
10. Resend email draft and confirmation flow
11. Docker and local run instructions

For each milestone, include exact files to create or modify, tests or manual verification steps, and a suggested git commit message. Do not mix unrelated features in the same milestone.
```

Suggested commit after this step:

```bash
git status
git add specs
git commit -m "tasks local FastAPI chatbot backend"
```

## 4. Full-Control Implementation

```text
/speckit-implement Take full control of the implementation.

Implement all milestones from tasks.md in order. For each milestone:

1. Implement the milestone completely.
2. Run the available build, test, or verification commands.
3. If verification passes, create a git commit for that milestone.
4. Use a clear commit message that describes only that milestone.
5. Continue automatically to the next milestone.

Rules:
- Keep each milestone as a separate commit.
- Do not combine unrelated milestones in one commit.
- Do not skip verification unless there is no available command.
- If verification fails, fix the issue and rerun verification before committing.
- If blocked by missing secrets such as OPENAI_API_KEY or RESEND_API_KEY, add placeholders to .env.example, document the requirement, and continue with mock-safe code where possible.
- Do not implement Google OAuth, Gmail, Google Drive, cloud deployment, rate limiting, or advanced logging in this version.
- Stop only if there is a real blocker that cannot be resolved locally.
```

## Optional Short Implementation Prompt

```text
/speckit-implement Implement the entire project from tasks.md without asking me between milestones. Commit after each milestone separately. Run verification before every commit. Fix failures before continuing. Only stop for real blockers.
```

## New Feature Requested: Telegram Long Polling Bot

Use this prompt when adding Telegram bot support after the base FastAPI chatbot backend is working.

```text
Implement Telegram long polling support for the local FastAPI chatbot backend.

Goal:
Allow one Telegram user to chat with the existing assistant through a Telegram bot using long polling, so it works locally in Docker without a public webhook URL.

Important:
Do not ask for or hardcode any real Telegram token, OpenAI key, Resend key, or other secret. I will add environment values manually. Only define the expected environment variable names in .env.example and documentation.

Scope:
- Add a Telegram bot worker service that runs alongside the FastAPI API in Docker Compose.
- Read TELEGRAM_BOT_TOKEN from the environment at runtime.
- Support optional TELEGRAM_ALLOWED_USER_IDS for restricting local testing to one or more Telegram user IDs.
- Reuse the existing chat/conversation logic where possible.
- Do not add Telegram webhooks in this version.
- Do not add Google OAuth, Gmail, Google Drive, cloud deployment, rate limiting, or advanced logging.

Behavior:
- When a Telegram message arrives, identify the Telegram user by Telegram user ID.
- For v1, auto-create or reuse a local user mapped to that Telegram user ID.
- Store Telegram conversations in the existing conversation/message tables where possible.
- Send the assistant response back to the Telegram chat.
- If TELEGRAM_ALLOWED_USER_IDS is set, reject messages from other users with a short “not authorized” reply.
- Handle /start with a short welcome message.
- Handle normal text messages as chat prompts.
- Ignore unsupported Telegram update types for now.
- If TELEGRAM_BOT_TOKEN is missing, the worker should fail fast with a clear startup error.

Environment:
Add placeholders only:
TELEGRAM_BOT_TOKEN=replace-with-telegram-bot-token
TELEGRAM_ALLOWED_USER_IDS=

Architecture:
- Add a worker entrypoint, for example app/telegram_worker.py.
- Add a Telegram service module, for example app/services/telegram.py.
- Add any needed database model/table for mapping telegram_user_id to local user_id.
- Update docker-compose.yml with a telegram worker service using the same image/build context and .env file.
- Keep the API service behavior unchanged except for shared model/service additions.

Verification:
- Add tests for:
  1. Telegram user mapping creation/reuse.
  2. Allowed user filtering.
  3. /start response.
  4. Text message routed into existing chat logic.
  5. Missing TELEGRAM_BOT_TOKEN produces a clear worker startup error.
- Do not make real Telegram network calls in tests; mock Telegram API calls.
- Run the full test suite.
- Validate docker compose config.

Commit:
Make one clean commit with message:
add Telegram long polling bot worker
```

## New Feature Requested: Telegram RAG Demo Documents And Profile Email

Use this prompt after the base Telegram long polling bot is working.

```text
Implement a complete local Telegram demo experience for the FastAPI chatbot backend.

Goal:
Allow any accepted Telegram user to chat with the bot using Grupo Pellas demo knowledge, receive cleanly formatted Telegram answers, and send a generated customer profile summary by email through Resend.

Important:
Do not ask for or hardcode real Telegram, OpenAI, or Resend secrets. Use existing environment variables only. Keep this local-first and Docker-friendly. Do not add Google OAuth, Gmail, Google Drive, cloud deployment, rate limiting, or advanced logging.

Demo Knowledge Base:
- Add local sample documents under sample_documents/.
- Include demo/fictitious Grupo Pellas vehicle, motorcycle, services, financing, warranty, branch, FAQ, products, accessories, and customer support information.
- Clearly mark the documents as demo data, not official Grupo Pellas information.
- Ensure Docker copies sample_documents into the image so seed scripts and the Telegram worker can read them.

Automatic RAG Seeding:
- Add a shared demo document seeding service.
- Every accepted Telegram user should automatically receive the demo RAG documents the first time they message the bot.
- Store the demo documents under that Telegram user’s internal app user, for example telegram_<telegram_user_id>.
- Make seeding idempotent, so repeated messages or repeated seed runs do not duplicate the same documents for the same user.
- Keep a manual seed command available for local testing:
  docker compose run --rm api python -m app.scripts.seed_grupo_pellas_demo
- The manual seed command should use TELEGRAM_ALLOWED_USER_IDS when present, otherwise known Telegram users already stored in SQLite.

Telegram RAG Behavior:
- When a Telegram user has document chunks, answer normal messages using the existing RAG search flow.
- Save Telegram user and assistant messages in the existing conversations/messages tables.
- Keep each Telegram user mapped to its own local user and conversation.
- If no documents are available, fall back to the normal chat behavior.

Telegram Formatting:
- Format outgoing Telegram responses so common Markdown does not appear raw.
- Convert Markdown headings like ### Title into plain Telegram-friendly headings.
- Convert **bold** into Telegram HTML bold.
- Escape unsafe HTML before sending.
- Send Telegram messages with parse_mode="HTML".

Profile Email Flow:
- Add a Telegram /send command.
- When the user sends /send, ask for the recipient email address.
- The next valid email address should immediately trigger the email send.
- Treat the user providing the email after /send as the explicit confirmation for this Telegram-only flow.
- Add /cancel to cancel a pending email send.
- Validate email format before sending.
- Build a concise customer profile summary from the Telegram user’s recent conversation history.
- The profile should include likely interests, requested products, questions, and next steps, without inventing personal data.
- Send the profile through the existing Resend email service.
- Store the email draft and send record using the existing email tables.
- If Resend fails, reply with a clear failure message.

Email Formatting:
- Format the generated profile email body as clean HTML before sending.
- Convert headings, bullet lists, and **bold** Markdown into HTML tags.
- Escape unsafe HTML before sending.
- Do not send raw Markdown symbols in the email body.

Conversation Reset Utility:
- It should be safe to clear only conversations and messages during local testing while preserving:
  users
  telegram_users
  documents
  document_chunks
- Reset telegram_users.conversation_id to null when clearing conversation history.

Tests:
- Add or update tests for:
  1. Automatic demo document seeding for a new Telegram user.
  2. Idempotent demo document seeding.
  3. Telegram RAG answers when documents exist.
  4. Telegram HTML response formatting.
  5. /send starts the email flow.
  6. Invalid recipient email is rejected.
  7. Valid recipient email sends the profile through the existing email service.
  8. /cancel clears the pending send state.
  9. Profile email HTML formatting.
  10. Docker Compose config remains valid.
- Do not make real Telegram, OpenAI, or Resend network calls in tests. Mock provider calls.
- Run the full test suite.

Docker:
- Rebuild and restart the api and telegram services after implementation:
  docker compose build api telegram
  docker compose up -d api telegram

Commit:
Do not commit automatically unless explicitly asked. Leave changes unstaged for review.
```
