from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.user import AuthContext, UserAdminCreate, UserRead, UserUpdate
from backend.services.user_service import (
    create_admin_managed_user,
    delete_user,
    get_user_or_404,
    list_users,
    require_admin,
    update_user,
)

router = APIRouter()


@router.get(
    "",
    response_model=list[UserRead],
    summary="List users",
    description="Admin-only endpoint that returns all registered users.",
    responses={
        200: {"description": "Users returned successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
    },
)
def get_users(
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> list[UserRead]:
    return [UserRead.model_validate(user) for user in list_users(db)]


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by id",
    description="Admin-only endpoint that returns one user record by numeric user id.",
    responses={
        200: {"description": "User returned successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
        404: {"description": "User was not found."},
    },
)
def get_user(
    user_id: int,
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserRead:
    return UserRead.model_validate(get_user_or_404(db, user_id))


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a managed user",
    description="Admin-only endpoint that creates a user with an explicit role and active status.",
    responses={
        201: {"description": "User created successfully."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
        409: {"description": "A user with the same email already exists."},
    },
)
def create_user(
    body: UserAdminCreate,
    _: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserRead:
    user = create_admin_managed_user(db, body)
    return UserRead.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Update a user",
    description=(
        "Admin-only endpoint that updates mutable user fields such as email, "
        "display name, password, role, and active status."
    ),
    responses={
        200: {"description": "User updated successfully."},
        400: {"description": "Protected self-action was blocked."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
        404: {"description": "User was not found."},
        409: {"description": "A user with the same email already exists."},
    },
)
def replace_user(
    user_id: int,
    body: UserUpdate,
    auth_context: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserRead:
    user = get_user_or_404(db, user_id)
    updated = update_user(db, user, body, acting_user=auth_context)
    return UserRead.model_validate(updated)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Admin-only endpoint that permanently deletes a user account.",
    responses={
        204: {"description": "User deleted successfully."},
        400: {"description": "Protected self-action was blocked."},
        401: {"description": "Token is missing, invalid, or expired."},
        403: {"description": "Admin access is required."},
        404: {"description": "User was not found."},
    },
)
def remove_user(
    user_id: int,
    auth_context: AuthContext = Depends(require_admin),
    db: Session = Depends(get_db),
) -> Response:
    user = get_user_or_404(db, user_id)
    delete_user(db, user, acting_user=auth_context)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
