from __future__ import annotations

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.config import AUTH_METHOD, AUTH_PROVIDER
from backend.core.security import decode_token, oauth2_scheme
from backend.db.session import get_db
from backend.models.user import User
from backend.schemas.user import AuthContext, UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, payload: UserCreate, password_hash: str) -> User:
    existing_user = get_user_by_email(db, payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=payload.email,
        display_name=payload.display_name,
        password_hash=password_hash,
        role="Employee",
        issuer=AUTH_PROVIDER,
        oidc_subject=None,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def build_auth_context(user: User, token_subject: str) -> AuthContext:
    return AuthContext(
        user_id=user.id,
        email=user.email,
        role=user.role,
        auth_method=AUTH_METHOD,
        token_subject=token_subject,
        provider=AUTH_PROVIDER,
        is_active=user.is_active,
    )


def get_current_auth_context(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    payload = decode_token(token)
    subject = str(payload["sub"])

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject is invalid.",
        ) from exc

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user was not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    return build_auth_context(user, token_subject=subject)
