"""Anonymous chat persistence and retention helpers.

The service stores chat ownership as a one-way HMAC instead of `user_id`. This
lets the backend find the current user's own chats without persisting a direct
foreign key from chat history to users. Message content is stored in masked form
only; raw user input should not be written through this service.
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.core.config import (
    CHAT_CONTEXT_MESSAGE_LIMIT,
    CHAT_CONTEXT_TTL_MINUTES,
    HISTORY_ANONYMIZATION_SECRET,
)
from backend.models.chat import Chat
from backend.models.message import Message
from backend.schemas.chat import ChatCreate, MessageCreate
from backend.schemas.user import AuthContext
from backend.pii_masker import mask_pii


def anonymous_user_key(auth_context: AuthContext) -> str:
    """Return a deterministic, non-reversible owner key for the current user."""
    payload = f"user:{auth_context.user_id}".encode("utf-8")
    secret = HISTORY_ANONYMIZATION_SECRET.encode("utf-8")
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def create_chat(
    db: Session,
    auth_context: AuthContext,
    payload: ChatCreate,
) -> Chat:
    """Create a new chat owned by the user's anonymous HMAC key."""
    title = mask_pii(payload.title) if payload.title else None
    chat = Chat(
        anonymous_user_key=anonymous_user_key(auth_context),
        title=title,
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def _normalize_datetime(value: object) -> datetime | None:
    """Normalize DB datetimes so TTL comparisons are timezone-safe."""
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def is_chat_active(chat: Chat) -> bool:
    """Check whether a chat is still inside the short multi-turn context window."""
    updated_at = _normalize_datetime(chat.updated_at)
    if updated_at is None:
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=CHAT_CONTEXT_TTL_MINUTES)
    return updated_at >= cutoff


def get_active_chat_or_404(
    db: Session,
    auth_context: AuthContext,
    chat_id: int,
) -> Chat:
    """Fetch a user's chat and reject it if the short session window expired."""
    chat = get_own_chat_or_404(db, auth_context, chat_id)
    if not is_chat_active(chat):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Chat session expired. Start a new chat.",
        )
    return chat


def get_or_create_active_chat(
    db: Session,
    auth_context: AuthContext,
    chat_id: int | None,
    title: str | None = None,
) -> Chat:
    """Reuse an active chat id or create a new chat when the frontend omits it."""
    if chat_id is not None:
        return get_active_chat_or_404(db, auth_context, chat_id)
    return create_chat(db, auth_context, ChatCreate(title=title))


def list_own_chats(db: Session, auth_context: AuthContext) -> list[Chat]:
    """Return all chats for the current user; kept for simple internal callers."""
    return (
        db.query(Chat)
        .filter(Chat.anonymous_user_key == anonymous_user_key(auth_context))
        .order_by(Chat.updated_at.desc(), Chat.id.desc())
        .all()
    )


def _apply_chat_date_filters(
    query,
    date_from: datetime | None,
    date_to: datetime | None,
):
    """Apply optional updated_at range filters to a Chat query."""
    if date_from is not None:
        query = query.filter(Chat.updated_at >= date_from)
    if date_to is not None:
        query = query.filter(Chat.updated_at <= date_to)
    return query


def _total_pages(total_items: int, page_size: int) -> int:
    """Calculate total pages for a Page-like API response."""
    if total_items == 0:
        return 0
    return ceil(total_items / page_size)


def paginate_own_chats(
    db: Session,
    auth_context: AuthContext,
    page: int,
    page_size: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> tuple[list[Chat], int, int]:
    """Return one page of the current user's chats and total counters."""
    query = db.query(Chat).filter(
        Chat.anonymous_user_key == anonymous_user_key(auth_context)
    )
    query = _apply_chat_date_filters(query, date_from, date_to)
    total_items = query.count()
    chats = (
        query.order_by(Chat.updated_at.desc(), Chat.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return chats, total_items, _total_pages(total_items, page_size)


def paginate_all_chats_for_admin(
    db: Session,
    page: int,
    page_size: int,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> tuple[list[tuple[Chat, int]], int, int]:
    """Return one admin page of anonymous chats with message counts."""
    filtered_chats = _apply_chat_date_filters(db.query(Chat), date_from, date_to)
    total_items = filtered_chats.count()
    chats_with_counts = (
        filtered_chats.outerjoin(Message, Message.chat_id == Chat.id)
        .group_by(Chat.id)
        .order_by(Chat.updated_at.desc(), Chat.id.desc())
        .with_entities(Chat, func.count(Message.id).label("message_count"))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return chats_with_counts, total_items, _total_pages(total_items, page_size)


def get_chat_or_404(db: Session, chat_id: int) -> Chat:
    """Fetch any chat by id for admin-only operations."""
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )
    return chat


def delete_chat_by_id(db: Session, chat_id: int) -> None:
    """Delete a chat and its messages via relationship cascade."""
    chat = get_chat_or_404(db, chat_id)
    db.delete(chat)
    db.commit()


def delete_expired_chats(db: Session, older_than_days: int) -> int:
    """Delete chats whose updated_at is older than the retention threshold."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
    expired_chats = db.query(Chat).filter(Chat.updated_at < cutoff).all()
    deleted_count = len(expired_chats)
    for chat in expired_chats:
        db.delete(chat)
    db.commit()
    return deleted_count


def get_own_chat_or_404(
    db: Session,
    auth_context: AuthContext,
    chat_id: int,
) -> Chat:
    """Fetch a chat only if it belongs to the current anonymous owner key."""
    chat = (
        db.query(Chat)
        .filter(
            Chat.id == chat_id,
            Chat.anonymous_user_key == anonymous_user_key(auth_context),
        )
        .first()
    )
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )
    return chat


def append_message(
    db: Session,
    auth_context: AuthContext,
    chat_id: int,
    payload: MessageCreate,
) -> Message:
    """Mask and persist a message, then bump the parent chat's updated_at."""
    chat = get_own_chat_or_404(db, auth_context, chat_id)
    content_masked = mask_pii(payload.content_masked)
    message = Message(
        chat_id=chat.id,
        sender_type=payload.sender_type,
        content_masked=content_masked,
    )
    chat.updated_at = datetime.now(timezone.utc)
    db.add(message)
    db.commit()
    db.refresh(message)
    db.refresh(chat)
    return message


def list_recent_messages_for_llm(
    chat: Chat,
    limit: int = CHAT_CONTEXT_MESSAGE_LIMIT,
) -> list[dict[str, str]]:
    """Build the masked prior-message list that is safe to send to the LLM."""
    messages = sorted(chat.messages, key=lambda message: message.created_at)[-limit:]
    return [
        {"role": message.sender_type, "content": message.content_masked}
        for message in messages
        if message.sender_type in {"user", "assistant", "system"}
    ]
