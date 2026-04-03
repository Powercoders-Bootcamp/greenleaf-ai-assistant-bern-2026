# Beat-Bot backend — quick start

This folder is a **FastAPI** service: it exposes `/chat`, calls **OpenAI** (GPT-4o by default), and runs tools (`check_holiday`, `search_handbook`) defined under `prompts/`. Data and prompts live **outside** this folder at the **repository root** (e.g. `data/`, `prompts/`), so always run the app from **`src/backend`** as below.

---

## Prerequisites

- **Python 3.10+** (3.11+ recommended)
- An **OpenAI API key** with **billing / quota** enabled (free tier exhaustion shows `429 insufficient_quota`)

---

## 1. Go to the backend folder

From the repo root:

```bash
cd src/backend
```

---

## 2. Create and activate a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a file named **`.env`** in **`src/backend/`** (same folder as `main.py`).

Minimal example:

```env
OPENAI_API_KEY=sk-...
```

Optional:

| Variable | Purpose |
|----------|---------|
| `OPENAI_MODEL` | Override model (default: `gpt-4o`) |
| `CORS_ORIGINS` | Comma-separated allowed origins (default: `*`) |

The app loads `.env` automatically via `python-dotenv`. Do **not** commit `.env` (it is gitignored).

---

## 5. Run the API

**Development** (auto-reload on code changes):

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should be able to open:

- **Interactive docs (Swagger UI):** http://127.0.0.1:8000/docs  
- **Health check:** http://127.0.0.1:8000/health  

---

## 6. Smoke test

**Health:**

```bash
curl -s http://127.0.0.1:8000/health
```

**Chat:**

```bash
curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello"}'
```

A successful response looks like: `{"reply":"..."}`.

---

## Common errors (quick reference)

| HTTP / symptom | Likely cause |
|----------------|--------------|
| `503` + `OPENAI_API_KEY is not configured` | Missing or empty `OPENAI_API_KEY` in `.env` (or server not restarted after editing `.env`) |
| `502` + `OpenAI error` + `429` / `insufficient_quota` | OpenAI account needs credits / billing; not a bug in this repo |
| `500` + `Server file or I/O error` | Missing repo files the backend reads (e.g. `prompts/system_prompt.txt`, handbook under `data/processed/`) — run from `src/backend` and ensure the **full repo** is present |
| JSON validation errors on `/chat` | Request body must be `{"message": "your text"}` with `Content-Type: application/json` |

---

## Project layout (backend-related)

| Path | Role |
|------|------|
| `main.py` | FastAPI app, `/health`, `/chat`, CORS |
| `chat_service.py` | OpenAI calls, tool loop, handbook search |
| `holidays_checker.py` | Holiday tool implementation |
| `../prompts/` (from repo root) | System prompt + tool JSON schemas |
| `../../data/` (from repo root) | Handbook and other data |

---

## Further reading (design / architecture)

- `docs/01-project-overview.md` — product goal and scope  
- `docs/08-backend-implementation-blueprint.md` — backend blueprint  
- `docs/22-backend-component-map.md` — component map  
