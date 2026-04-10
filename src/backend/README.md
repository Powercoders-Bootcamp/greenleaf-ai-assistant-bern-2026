# Beat-Bot Backend Quick Start

This folder contains the FastAPI backend for GreenLeaf Beat-Bot. It exposes authenticated chat, auth/user management, anonymous chat history, and LLM tool orchestration for `check_holiday` and `search_handbook`.

Data and prompts live at the repository root, for example `data/` and `prompts/`.

## Prerequisites

- Python 3.10+.
- PostgreSQL running locally or in Docker Compose.
- An OpenAI/OpenRouter-compatible API key configured as `OPENAI_API_KEY`.

## Install

From the repository root:

```powershell
cd src\backend
python -m venv myenv
.\myenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Environment

Create `src/backend/.env`.

```env
DATABASE_URL=postgresql+psycopg://appuser:apppassword@localhost:5432/appdb
OPENAI_API_KEY=sk-...
SECRET_KEY=change-me
HISTORY_ANONYMIZATION_SECRET=change-me
SUPERADMIN_EMAIL=superadmin@greenleaf.ch
SUPERADMIN_PASSWORD=ChangeThisSuperAdmin123!
SUPERADMIN_DISPLAY_NAME=GreenLeaf Superadmin
```

Useful optional settings:

| Variable | Purpose |
|----------|---------|
| `OPENAI_MODEL` | Override model, default is `gpt-4o`. |
| `CORS_ORIGINS` | Comma-separated allowed origins, default is `*`. |
| `CHAT_CONTEXT_TTL_MINUTES` | Active multi-turn chat window, default is `30`. |
| `CHAT_CONTEXT_MESSAGE_LIMIT` | Number of masked prior messages sent to the LLM, default is `12`. |
| `AUTO_CREATE_DB_TABLES` | Emergency local fallback for `Base.metadata.create_all`; keep `false` and use Alembic. |

Do not commit `.env`.

## Database Migrations

Schema changes are managed by Alembic. From `src/backend`:

```powershell
.\myenv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
```

The initial migration creates `users`, `chats`, and `messages`. It uses `IF NOT EXISTS` guards so it can safely mark an existing local dev database as migrated.

## Run The API

Run Uvicorn from `src` so `backend.*` package imports resolve correctly:

```powershell
cd .. 
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Chat Smoke Test

Log in first via `/auth/login`, then call `/chat` with the bearer token.

```powershell
curl -X POST http://127.0.0.1:8000/chat `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer <token>" `
  -d "{\"message\":\"Hello\"}"
```

A successful response looks like:

```json
{"chat_id":1,"reply":"..."}
```

To continue the same open frontend chat session, send the returned `chat_id`. If the page is refreshed, the frontend drops `chat_id` from memory and a new chat starts.

## Common Errors

| HTTP / symptom | Likely cause |
|----------------|--------------|
| `503` + `OPENAI_API_KEY is not configured` | Missing or empty `OPENAI_API_KEY` in `.env`, or server not restarted after editing `.env`. |
| `502` + `OpenAI error` | OpenAI/OpenRouter network, auth, quota, or rate-limit issue. |
| `409` on `/chat` | The frontend sent an expired `chat_id`; start a new chat without `chat_id`. |
| `500` + `Server file or I/O error` | Missing repo files such as `prompts/system_prompt.txt` or `data/processed/handbook-key-rules.md`. |
| Import error for `backend` | Run Uvicorn from `src` with `uvicorn backend.main:app --reload`. |

## Project Layout

| Path | Role |
|------|------|
| `main.py` | FastAPI app bootstrap, routers, CORS, superadmin seed. |
| `api/routes/chat.py` | Authenticated `/chat`, anonymous history persistence, PII-masked multi-turn flow. |
| `services/chat_service.py` | OpenAI/OpenRouter calls, tool loop, handbook search. |
| `services/chat_history_service.py` | Anonymous HMAC owner key, chat session TTL, masked message persistence. |
| `migrations/` | Alembic database migrations. |
| `holidays_checker.py` | Holiday tool implementation. |
