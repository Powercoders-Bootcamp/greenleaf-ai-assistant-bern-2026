from __future__ import annotations

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.config import (
    AUTH_METHOD,
    AUTH_PROVIDER,
    SUPERADMIN_DISPLAY_NAME,
    SUPERADMIN_EMAIL,
    SUPERADMIN_PASSWORD,
)
from backend.core.security import decode_token, hash_password, oauth2_scheme
from backend.db.session import get_db
from backend.models.user import User
from backend.schemas.user import AuthContext, UserAdminCreate, UserCreate, UserUpdate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def create_user(db: Session, payload: UserCreate, password_hash: str) -> User:
    return create_user_with_role(
        db=db,
        payload=payload,
        password_hash=password_hash,
        role="Employee",
    )


def create_user_with_role(
    db: Session,
    payload: UserCreate,
    password_hash: str,
    role: str,
    is_active: bool = True,
) -> User:
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
        role=role,
        issuer=AUTH_PROVIDER,
        oidc_subject=None,
        is_active=is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_superadmin(db: Session) -> User | None:
    if not SUPERADMIN_EMAIL:
        return None

    if not SUPERADMIN_PASSWORD:
        raise RuntimeError(
            "SUPERADMIN_PASSWORD must be set when SUPERADMIN_EMAIL is configured."
        )

    existing_user = get_user_by_email(db, SUPERADMIN_EMAIL)
    if existing_user is not None:
        if existing_user.role != "Admin":
            existing_user.role = "Admin"
            db.commit()
            db.refresh(existing_user)
        return existing_user

    payload = UserCreate(
        email=SUPERADMIN_EMAIL,
        display_name=SUPERADMIN_DISPLAY_NAME,
        password=SUPERADMIN_PASSWORD,
    )
    return create_user_with_role(
        db=db,
        payload=payload,
        password_hash=hash_password(SUPERADMIN_PASSWORD),
        role="Admin",
    )


def create_admin_managed_user(db: Session, payload: UserAdminCreate) -> User:
    return create_user_with_role(
        db=db,
        payload=payload,
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=payload.is_active,
    )


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


def get_user_or_404(db: Session, user_id: int) -> User:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


def update_user(
    db: Session,
    target_user: User,
    payload: UserUpdate,
    acting_user: AuthContext,
) -> User:
    if payload.email is not None and payload.email != target_user.email:
        existing = get_user_by_email(db, payload.email)
        if existing is not None and existing.id != target_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )
        target_user.email = payload.email

    if payload.display_name is not None:
        target_user.display_name = payload.display_name

    if payload.password is not None:
        target_user.password_hash = hash_password(payload.password)

    if payload.role is not None:
        if target_user.id == acting_user.user_id and payload.role != "Admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot remove your own admin role.",
            )
        target_user.role = payload.role

    if payload.is_active is not None:
        if target_user.id == acting_user.user_id and payload.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot deactivate your own account.",
            )
        target_user.is_active = payload.is_active

    db.commit()
    db.refresh(target_user)
    return target_user


def delete_user(db: Session, target_user: User, acting_user: AuthContext) -> None:
    if target_user.id == acting_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account.",
        )

    db.delete(target_user)
    db.commit()


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


def require_admin(
    auth_context: AuthContext = Depends(get_current_auth_context),
) -> AuthContext:
    if auth_context.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is required.",
        )
    return auth_context
