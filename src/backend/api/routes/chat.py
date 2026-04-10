"""Authenticated LLM chat endpoint.

This route is the main frontend chat entry point. It deliberately keeps only a
short-lived multi-turn context: the frontend sends the in-memory `chat_id` while
the page is open, and the backend rejects expired sessions. Messages are stored
through the anonymous history service, which masks PII before persistence and
before the text is sent to the LLM.
"""

from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAIError
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.chat import ChatTurnRequest, ChatTurnResponse, MessageCreate
from backend.schemas.user import AuthContext
from backend.services.chat_history_service import (
    append_message,
    get_or_create_active_chat,
    list_recent_messages_for_llm,
)
from backend.services.chat_service import run_chat
from backend.services.user_service import get_current_auth_context

logger = logging.getLogger(__name__)
router = APIRouter()


def _chat_title(message: str) -> str:
    """Create a compact title from the first user turn for admin/history lists."""
    compact = " ".join(message.split())
    return compact[:80] if compact else "New chat"


@router.post(
    "",
    response_model=ChatTurnResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Beat-Bot",
    description=(
        "Authenticated chat endpoint. The backend stores chat history under an "
        "anonymous HMAC owner key, masks PII before persistence and LLM calls, "
        "and only uses the current short-lived frontend chat session as context."
    ),
    responses={
        200: {
            "description": "Successful reply from the assistant.",
            "content": {
                "application/json": {
                    "example": {
                        "chat_id": 42,
                        "reply": "Hello, how can I help today?",
                    }
                }
            },
        },
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Authenticated user is inactive."},
        409: {"description": "The provided chat session expired."},
        503: {"description": "OpenAI is not configured (missing API key)."},
        502: {"description": "OpenAI API error (network, auth, rate limit, etc.)."},
        500: {"description": "Unexpected server error."},
    },
)
def chat(
    body: ChatTurnRequest,
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> ChatTurnResponse:
    """Run one chat turn and persist the masked user/assistant messages."""
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured on the server.",
        )

    chat_record = get_or_create_active_chat(
        db,
        auth_context,
        chat_id=body.chat_id,
        title=_chat_title(body.message),
    )
    # Load context before writing the new turn so the LLM sees prior messages
    # plus the current user message exactly once.
    prior_messages = list_recent_messages_for_llm(chat_record)

    user_message = append_message(
        db,
        auth_context,
        chat_record.id,
        MessageCreate(sender_type="user", content_masked=body.message),
    )

    try:
        reply = run_chat(
            user_message.content_masked,
            conversation_messages=prior_messages,
        )
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

    append_message(
        db,
        auth_context,
        chat_record.id,
        MessageCreate(sender_type="assistant", content_masked=reply),
    )

    return ChatTurnResponse(chat_id=chat_record.id, reply=reply)
