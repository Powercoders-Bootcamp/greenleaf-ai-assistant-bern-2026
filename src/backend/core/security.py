from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext

from backend.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, SECRET_KEY


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str | None) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    data: dict[str, str],
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        ) from exc
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
        )

    return payload
