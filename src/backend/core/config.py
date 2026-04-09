from __future__ import annotations

import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

AUTH_METHOD = os.getenv("AUTH_METHOD", "jwt")
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "local-dev")
