from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


UserRole = Literal["Employee", "Admin"]


class UserBase(BaseModel):
    email: EmailStr
    display_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AuthContext(BaseModel):
    user_id: int
    email: EmailStr
    role: UserRole
    auth_method: str
    token_subject: str
    provider: str
    is_active: bool
