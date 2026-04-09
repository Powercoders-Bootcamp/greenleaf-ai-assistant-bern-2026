"""Authentication and self-service account routes.

Registration is intentionally admin-gated in this project. Regular users can
log in, inspect their auth context/profile, and update only their own password.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.auth import (
    LoginRequest,
    PasswordChangeRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.schemas.user import AuthContext, UserRead
from backend.services.auth_service import change_user_password, login_user, register_user
from backend.services.user_service import (
    get_current_auth_context,
    get_user_by_id,
    require_admin,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new employee account",
    description="Admin-only endpoint that creates a new user account with the default `Employee` role.",
    responses={
        201: {
            "description": "User account created successfully.",
        },
        401: {
            "description": "Token is missing, invalid, or expired.",
        },
        403: {
            "description": "Admin access is required.",
        },
        409: {
            "description": "A user with the same email already exists.",
        },
    },
)
def register(
    body: RegisterRequest,
    _: AuthContext = Depends(require_admin),
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


@router.put(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change current user password",
    description="Allows any authenticated active user to update only their own password.",
    responses={
        204: {"description": "Password updated successfully."},
        401: {"description": "Token is invalid or current password is wrong."},
        403: {"description": "Authenticated user is inactive."},
    },
)
def change_password(
    body: PasswordChangeRequest,
    auth_context: AuthContext = Depends(get_current_auth_context),
    db: Session = Depends(get_db),
) -> Response:
    user = get_user_by_id(db, auth_context.user_id)
    change_user_password(db, user, body)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
