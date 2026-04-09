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
    summary="Register a new employee account",
    description="Creates a new user account with the default `Employee` role.",
    responses={
        201: {
            "description": "User account created successfully.",
        },
        409: {
            "description": "A user with the same email already exists.",
        },
    },
)
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserRead:
    user = register_user(db, body)
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate a user",
    description="Validates user credentials and returns a bearer token plus the resolved user profile.",
    responses={
        200: {"description": "Authentication succeeded."},
        401: {"description": "Credentials are invalid."},
        403: {"description": "The user account exists but is inactive."},
    },
)
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user, token = login_user(db, body.email, body.password)
    return TokenResponse(access_token=token, user=UserRead.model_validate(user))


@router.get(
    "/me",
    response_model=AuthContext,
    summary="Get current auth context",
    description="Returns the normalized authentication context derived from the bearer token.",
    responses={
        200: {"description": "Authenticated user context returned."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Authenticated user is inactive."},
    },
)
def me(
    auth_context: AuthContext = Depends(get_current_auth_context),
) -> AuthContext:
    return auth_context


@router.get(
    "/profile",
    response_model=UserRead,
    summary="Get current user profile",
    description="Returns the persisted user profile for the currently authenticated user.",
    responses={
        200: {"description": "User profile returned."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Authenticated user is inactive."},
    },
)
def profile(
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> UserRead:
    user = get_user_by_id(db, auth_context.user_id)
    return UserRead.model_validate(user)
