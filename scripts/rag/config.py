from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_OPENAI_EMBEDDING_MODELS = {
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
}

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "greenleaf_handbook")
DEFAULT_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
DEFAULT_DOCUMENT_TYPE = "handbook"

DEFAULT_MAX_WORDS = 220
DEFAULT_OVERLAP_WORDS = 40
DEFAULT_MIN_CHUNK_WORDS = 30