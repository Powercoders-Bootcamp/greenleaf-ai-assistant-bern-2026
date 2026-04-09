from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from backend.schemas.user import UserRead


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "employee@greenleaf.ch",
                "password": "supersecret",
            }
        }
    }


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str | None = Field(default=None, max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "new.user@greenleaf.ch",
                "password": "ChangeMe123!",
                "display_name": "New User",
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "employee@greenleaf.ch",
                    "display_name": "Green Leaf Employee",
                    "role": "Employee",
                    "is_active": True,
                    "created_at": "2026-04-09T12:00:00Z",
                    "updated_at": "2026-04-09T12:00:00Z",
                },
            }
        }
    }
