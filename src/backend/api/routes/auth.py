from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from backend.schemas.user import AuthContext, UserRead
from backend.services.auth_service import login_user, register_user
from backend.services.user_service import get_current_auth_context, get_user_by_id

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserRead:
    user = register_user(db, body)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user, token = login_user(db, body.email, body.password)
    return TokenResponse(access_token=token, user=UserRead.model_validate(user))


@router.get("/me", response_model=AuthContext)
def me(
    auth_context: AuthContext = Depends(get_current_auth_context),
) -> AuthContext:
    return auth_context


@router.get("/profile", response_model=UserRead)
def profile(
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> UserRead:
    user = get_user_by_id(db, auth_context.user_id)
    return UserRead.model_validate(user)
