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


class UserAdminCreate(UserCreate):
    role: UserRole = "Employee"
    is_active: bool = True

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "managed.user@greenleaf.ch",
                "display_name": "Managed User",
                "password": "ChangeMe123!",
                "role": "Employee",
                "is_active": True,
            }
        }
    }


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

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "email": "admin@greenleaf.ch",
                "role": "Admin",
                "auth_method": "jwt",
                "token_subject": "1",
                "provider": "docker-postgres-local",
                "is_active": True,
            }
        }
    }


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None
    is_active: bool | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "display_name": "Updated Managed User",
                "role": "Admin",
                "is_active": True,
            }
        }
    }
