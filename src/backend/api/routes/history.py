"""Current user's anonymous chat history endpoints.

These endpoints are scoped to the authenticated user's HMAC-derived anonymous
owner key. They do not expose user ids, emails, or the anonymous key itself.
Admin-wide history management lives under `/admin/chats`.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.chat import (
    ChatCreate,
    ChatDetail,
    ChatPage,
    ChatRead,
    MessageCreate,
    MessageRead,
)
from backend.schemas.user import AuthContext
from backend.services.chat_history_service import (
    append_message,
    create_chat,
    get_own_chat_or_404,
    paginate_own_chats,
)
from backend.services.user_service import get_current_auth_context

router = APIRouter()


@router.post(
    "",
    response_model=ChatRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create anonymous chat history entry",
    description=(
        "Creates a chat record owned by an anonymous HMAC key. "
        "No user_id or email is persisted."
    ),
)
def create_history_chat(
    body: ChatCreate,
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> ChatRead:
    """Create a chat record for the current anonymous owner key."""
    chat = create_chat(db, auth_context, body)
    return ChatRead.model_validate(chat)


@router.get(
    "",
    response_model=ChatPage,
    summary="List own anonymous chat history",
    description=(
        "Returns chats matching the current user's anonymous HMAC key. "
        "The key is never returned in the API response. Supports page-based "
        "pagination and optional updated_at date range filters."
    ),
)
def get_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> ChatPage:
    """Return current user's chats as a page with optional updated_at filters."""
    chats, total_items, total_pages = paginate_own_chats(
        db,
        auth_context,
        page=page,
        page_size=page_size,
        date_from=date_from,
        date_to=date_to,
    )
    return ChatPage(
        items=[ChatRead.model_validate(chat) for chat in chats],
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
    )


@router.get(
    "/{chat_id}",
    response_model=ChatDetail,
    summary="Get own anonymous chat history detail",
    description="Returns one chat and its messages only if it belongs to the current anonymous user key.",
)
def get_history_chat(
    chat_id: int,
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> ChatDetail:
    """Return a single chat only if it belongs to the current anonymous owner."""
    chat = get_own_chat_or_404(db, auth_context, chat_id)
    return ChatDetail.model_validate(chat)


@router.post(
    "/{chat_id}/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
    summary="Append message to own anonymous chat",
    description=(
        "Persists a message under the current user's anonymous chat. "
        "PII masking is applied before storage."
    ),
)
def create_history_message(
    chat_id: int,
    body: MessageCreate,
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> MessageRead:
    """Append a masked message to the current user's anonymous chat."""
    message = append_message(db, auth_context, chat_id, body)
    return MessageRead.model_validate(message)
