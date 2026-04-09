"""
GreenLeaf Beat-Bot API — chat endpoint for the frontend (OpenAI GPT-4o + tools).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAIError
from starlette.responses import RedirectResponse

from backend.services.chat_service import run_chat
from backend.api.routes import auth
from backend.core.config import DATABASE_URL
from backend.db.base import Base
from backend.db.session import engine
from backend.models.user import User

load_dotenv(Path(__file__).resolve().parent / ".env")

logger = logging.getLogger(__name__)


def _safe_database_target(database_url: str) -> str:
    if "@" in database_url:
        return database_url.split("@", 1)[1]
    return database_url

Base.metadata.create_all(bind=engine)
logger.info("Database configured for %s", _safe_database_target(DATABASE_URL))

app = FastAPI(
    title="GreenLeaf Beat-Bot API",
    version="0.1.0",
    description=(
        "Internal assistant backend. Send a user message; the server calls "
        "OpenAI GPT-4o with registered tools (`check_holiday`, `search_handbook`) "
        "and returns the assistant reply."
    ),
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Payload from the frontend: a single user turn."""

    message: str = Field(
        ...,
        min_length=1,
        description="End-user text (e.g. greeting or HR/holiday question).",
        examples=["Hello", "Is 2026-05-01 a public holiday in Basel?"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "Hello"}],
        }
    }


class ChatResponse(BaseModel):
    """Assistant reply after the LLM (and any tool runs) finishes."""

    reply: str = Field(..., description="Beat-Bot answer to show in the UI.")


@app.get("/health", summary="Health check", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/swagger", include_in_schema=False)
@app.get("/swagger/", include_in_schema=False)
def swagger_redirect() -> RedirectResponse:
    """FastAPI serves Swagger UI at `/docs`, not `/swagger`. This redirects for convenience."""
    return RedirectResponse(url="/docs", status_code=307)


@app.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Beat-Bot",
    tags=["chat"],
    responses={
        200: {
            "description": "Successful reply from the assistant.",
            "content": {
                "application/json": {
                    "example": {"reply": "Hello — how can I help today?"}
                }
            },
        },
        503: {"description": "OpenAI is not configured (missing API key)."},
        502: {"description": "OpenAI API error (network, auth, rate limit, etc.)."},
        500: {"description": "Unexpected server error (e.g. missing data file)."},
    },
)
def chat(body: ChatRequest) -> ChatResponse:
    """
    Forward the user message to GPT-4o. The model may call tools; the backend
    executes them and returns the final natural-language answer.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured on the server.",
        )
    try:
        reply = run_chat(body.message)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except OpenAIError as exc:
        msg = str(exc).strip() or "OpenAI request failed."
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI error: {msg}",
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server file or I/O error: {exc}",
        ) from exc
    except Exception as exc:
        logger.exception("Unhandled error in /chat")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error. See server logs for details.",
        ) from exc
    return ChatResponse(reply=reply)
