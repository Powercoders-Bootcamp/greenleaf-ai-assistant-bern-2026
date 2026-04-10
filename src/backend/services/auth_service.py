from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.core.security import create_access_token, hash_password, verify_password
from backend.models.user import User
from backend.schemas.auth import PasswordChangeRequest, RegisterRequest
from backend.schemas.user import UserCreate
from backend.services.user_service import create_user, get_user_by_email


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


def register_user(db: Session, body: RegisterRequest) -> User:
    payload = UserCreate(
        email=body.email,
        display_name=body.display_name,
        password=body.password,
    )
    return create_user(db, payload, password_hash=hash_password(body.password))


def login_user(db: Session, email: str, password: str) -> tuple[User, str]:
    user = authenticate_user(db, email, password)
    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )
    return user, token


def change_user_password(
    db: Session,
    user: User,
    body: PasswordChangeRequest,
) -> None:
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is invalid",
        )

    user.password_hash = hash_password(body.new_password)
    db.commit()
