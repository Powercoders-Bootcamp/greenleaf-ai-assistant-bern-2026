"""Pydantic schemas for anonymous chat, history, and chat API responses."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SenderType = Literal["user", "assistant", "system"]


class MessageCreate(BaseModel):
    """Inbound message payload; content is expected to be masked before storage."""

    sender_type: SenderType
    content_masked: str = Field(min_length=1)


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    sender_type: SenderType
    content_masked: str
    created_at: datetime


class ChatCreate(BaseModel):
    title: str | None = Field(default=None, max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Vacation policy question",
            }
        }
    }


class ChatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


class AdminChatRead(ChatRead):
    message_count: int = 0


class AdminChatDetail(AdminChatRead):
    messages: list[MessageRead] = []


class ChatPage(BaseModel):
    """Spring Page-like response for the current user's chat history."""

    items: list[ChatRead]
    page: int
    page_size: int
    total_items: int
    total_pages: int


class AdminChatPage(BaseModel):
    """Spring Page-like response for admin chat management."""

    items: list[AdminChatRead]
    page: int
    page_size: int
    total_items: int
    total_pages: int


class ChatRetentionCleanupResponse(BaseModel):
    deleted_count: int


class ChatDetail(ChatRead):
    messages: list[MessageRead] = []


class ChatTurnRequest(BaseModel):
    """One frontend chat turn; `chat_id` is ephemeral browser state."""

    message: str = Field(
        ...,
        min_length=1,
        description="Current user turn. The backend masks PII before sending it to the LLM.",
        examples=["Is 2026-05-01 a public holiday in Basel?"],
    )
    chat_id: int | None = Field(
        default=None,
        description=(
            "Ephemeral frontend chat session id. Omit it to start a new anonymous chat."
        ),
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"message": "Hello"},
                {"chat_id": 12, "message": "What about the Friday after that?"},
            ],
        }
    }


class ChatTurnResponse(BaseModel):
    """LLM answer plus the chat id to reuse while the page remains open."""

    chat_id: int = Field(
        ...,
        description="Anonymous chat id to reuse only while the current frontend chat UI stays open.",
    )
    reply: str = Field(..., description="Beat-Bot answer to show in the UI.")
