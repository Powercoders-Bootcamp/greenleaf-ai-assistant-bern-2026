from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
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
    payload = f"user:{auth_context.user_id}".encode("utf-8")
    secret = HISTORY_ANONYMIZATION_SECRET.encode("utf-8")
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def create_chat(
    db: Session,
    auth_context: AuthContext,
    payload: ChatCreate,
) -> Chat:
    chat = Chat(
        anonymous_user_key=anonymous_user_key(auth_context),
        title=payload.title,
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def _normalize_datetime(value: object) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def is_chat_active(chat: Chat) -> bool:
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
    if chat_id is not None:
        return get_active_chat_or_404(db, auth_context, chat_id)
    return create_chat(db, auth_context, ChatCreate(title=title))


def list_own_chats(db: Session, auth_context: AuthContext) -> list[Chat]:
    return (
        db.query(Chat)
        .filter(Chat.anonymous_user_key == anonymous_user_key(auth_context))
        .order_by(Chat.updated_at.desc(), Chat.id.desc())
        .all()
    )


def get_own_chat_or_404(
    db: Session,
    auth_context: AuthContext,
    chat_id: int,
) -> Chat:
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
    messages = sorted(chat.messages, key=lambda message: message.created_at)[-limit:]
    return [
        {"role": message.sender_type, "content": message.content_masked}
        for message in messages
        if message.sender_type in {"user", "assistant", "system"}
    ]
