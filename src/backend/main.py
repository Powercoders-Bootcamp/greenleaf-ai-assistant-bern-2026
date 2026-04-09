"""
GreenLeaf Beat-Bot API - FastAPI application bootstrap.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from backend.api.routes import auth, chat, history, users
from backend.core.config import AUTO_CREATE_DB_TABLES, DATABASE_URL
from backend.db.base import Base
from backend.db.session import SessionLocal, engine
from backend.models.chat import Chat
from backend.models.message import Message
from backend.models.user import User
from backend.services.user_service import ensure_superadmin

load_dotenv(Path(__file__).resolve().parent / ".env")

logger = logging.getLogger(__name__)


def _safe_database_target(database_url: str) -> str:
    if "@" in database_url:
        return database_url.split("@", 1)[1]
    return database_url


if AUTO_CREATE_DB_TABLES:
    Base.metadata.create_all(bind=engine)
else:
    logger.info("Database table creation is managed by Alembic migrations.")

logger.info("Database configured for %s", _safe_database_target(DATABASE_URL))

with SessionLocal() as db:
    seeded_superadmin = ensure_superadmin(db)
    if seeded_superadmin is not None:
        logger.info("Superadmin ready for %s", seeded_superadmin.email)

app = FastAPI(
    title="GreenLeaf Beat-Bot API",
    version="0.1.0",
    description=(
        "Internal assistant backend. Send a user message; the server calls "
        "OpenAI with registered tools (`check_holiday`, `search_handbook`) "
        "and returns the assistant reply."
    ),
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(history.router, prefix="/history", tags=["history"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health check", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/swagger", include_in_schema=False)
@app.get("/swagger/", include_in_schema=False)
def swagger_redirect() -> RedirectResponse:
    """FastAPI serves Swagger UI at `/docs`, not `/swagger`."""
    return RedirectResponse(url="/docs", status_code=307)
