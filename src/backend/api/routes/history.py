from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.chat import ChatCreate, ChatDetail, ChatRead, MessageCreate, MessageRead
from backend.schemas.user import AuthContext
from backend.services.chat_history_service import (
    append_message,
    create_chat,
    get_own_chat_or_404,
    list_own_chats,
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
    chat = create_chat(db, auth_context, body)
    return ChatRead.model_validate(chat)


@router.get(
    "",
    response_model=list[ChatRead],
    summary="List own anonymous chat history",
    description=(
        "Returns chats matching the current user's anonymous HMAC key. "
        "The key is never returned in the API response."
    ),
)
def get_history(
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> list[ChatRead]:
    return [ChatRead.model_validate(chat) for chat in list_own_chats(db, auth_context)]


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
    message = append_message(db, auth_context, chat_id, body)
    return MessageRead.model_validate(message)
