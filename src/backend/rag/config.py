from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = Path(os.getenv("VECTOR_DB_DIR", BASE_DIR / "chroma_db"))
COLLECTION_NAME = os.getenv("HANDBOOK_COLLECTION_NAME", "handbook")
EMBEDDING_MODEL = os.getenv("HANDBOOK_EMBEDDING_MODEL", "text-embedding-3-small")
ALLOWED_EMBEDDING_MODELS = {
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
}
DEFAULT_TOP_K = int(os.getenv("HANDBOOK_TOP_K", "4"))
