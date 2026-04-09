from __future__ import annotations

import hashlib
import hmac

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.core.config import HISTORY_ANONYMIZATION_SECRET
from backend.models.chat import Chat
from backend.models.message import Message
from backend.schemas.chat import ChatCreate, MessageCreate
from backend.schemas.user import AuthContext


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
    message = Message(
        chat_id=chat.id,
        sender_type=payload.sender_type,
        # TODO: apply pii_masker before persistence.
        content_masked=payload.content_masked,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    db.refresh(chat)
    return message
