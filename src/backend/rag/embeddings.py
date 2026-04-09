from __future__ import annotations

import os
from langchain_openai import OpenAIEmbeddings

DEFAULT_EMBEDDING_MODEL = "openai/text-embedding-3-small"

def get_embeddings(model: str | None = None) -> OpenAIEmbeddings:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing.")

    return OpenAIEmbeddings(
        model=model or DEFAULT_EMBEDDING_MODEL,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        tiktoken_enabled=True,
        tiktoken_model_name="text-embedding-3-small",
    )