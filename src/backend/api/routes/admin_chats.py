from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.chat import (
    AdminChatPage,
    AdminChatRead,
    ChatRetentionCleanupResponse,
)
from backend.schemas.user import AuthContext
from backend.services.chat_history_service import (
    delete_chat_by_id,
    delete_expired_chats,
    paginate_all_chats_for_admin,
)
from backend.services.user_service import require_admin

router = APIRouter()


@router.get(
    "/chats",
    response_model=AdminChatPage,
    summary="List anonymous chats",
    description=(
        "Admin-only endpoint that lists anonymous chat records without exposing "
        "anonymous owner keys or user identifiers. Supports page-based pagination "
        "and optional updated_at date range filters."
    ),
    responses={
        200: {"description": "Anonymous chat records returned successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
    },
)
def get_admin_chats(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> AdminChatPage:
    chats, total_items, total_pages = paginate_all_chats_for_admin(
        db,
        page=page,
        page_size=page_size,
        date_from=date_from,
        date_to=date_to,
    )
    return AdminChatPage(
        items=[
            AdminChatRead(
                id=chat.id,
                title=chat.title,
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                message_count=message_count,
            )
            for chat, message_count in chats
        ],
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
    )


@router.delete(
    "/chats/expired",
    response_model=ChatRetentionCleanupResponse,
    summary="Delete expired anonymous chats",
    description=(
        "Admin-only retention cleanup endpoint. Deletes anonymous chats whose "
        "`updated_at` timestamp is older than the requested number of days."
    ),
    responses={
        200: {"description": "Expired chats deleted successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
    },
)
def remove_expired_admin_chats(
    older_than_days: int = Query(default=30, ge=1, le=3650),
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ChatRetentionCleanupResponse:
    deleted_count = delete_expired_chats(db, older_than_days=older_than_days)
    return ChatRetentionCleanupResponse(deleted_count=deleted_count)


@router.delete(
    "/chats/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete anonymous chat",
    description="Admin-only endpoint that deletes any anonymous chat and its messages.",
    responses={
        204: {"description": "Anonymous chat deleted successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
        404: {"description": "Chat was not found."},
    },
)
def remove_admin_chat(
    chat_id: int,
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Response:
    delete_chat_by_id(db, chat_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
