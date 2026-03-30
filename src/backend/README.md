# Backend

FastAPI backend for the GreenLeaf assistant.

## Current MVP

- `GET /` health check
- `POST /ask` endpoint
- request validation with Pydantic
- structured mock response with sources
- safe invalid input handling
- Swagger docs at `/docs`

## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000