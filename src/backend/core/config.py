from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required.")

if not DATABASE_URL.startswith("postgresql+psycopg://"):
    raise RuntimeError(
        "Only PostgreSQL connections using the psycopg driver are supported."
    )

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me-32chars")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

AUTH_METHOD = os.getenv("AUTH_METHOD", "jwt")
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "local-dev")
AUTO_CREATE_DB_TABLES = os.getenv("AUTO_CREATE_DB_TABLES", "false").lower() == "true"

SUPERADMIN_EMAIL = os.getenv("SUPERADMIN_EMAIL")
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD")
SUPERADMIN_DISPLAY_NAME = os.getenv("SUPERADMIN_DISPLAY_NAME", "Super Admin")

HISTORY_ANONYMIZATION_SECRET = os.getenv("HISTORY_ANONYMIZATION_SECRET")
if not HISTORY_ANONYMIZATION_SECRET:
    raise RuntimeError("HISTORY_ANONYMIZATION_SECRET is required.")

CHAT_CONTEXT_TTL_MINUTES = int(os.getenv("CHAT_CONTEXT_TTL_MINUTES", "30"))
CHAT_CONTEXT_MESSAGE_LIMIT = int(os.getenv("CHAT_CONTEXT_MESSAGE_LIMIT", "12"))
