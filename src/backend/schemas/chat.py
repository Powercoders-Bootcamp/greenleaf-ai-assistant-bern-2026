from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SenderType = Literal["user", "assistant", "system"]


class MessageCreate(BaseModel):
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


class ChatDetail(ChatRead):
    messages: list[MessageRead] = []
