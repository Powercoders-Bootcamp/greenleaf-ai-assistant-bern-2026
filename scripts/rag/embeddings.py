from __future__ import annotations

from sentence_transformers import SentenceTransformer
from openai import OpenAI

from config import SUPPORTED_OPENAI_EMBEDDING_MODELS


class LocalEmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, query: str) -> list[float]:
        return self.model.encode([query])[0].tolist()


class OpenAIEmbeddingService:
    def __init__(self, model: str, api_key: str | None = None) -> None:
        if model not in SUPPORTED_OPENAI_EMBEDDING_MODELS:
            raise ValueError(
                f"Unsupported embedding model: {model}. "
                f"Choose one of: {sorted(SUPPORTED_OPENAI_EMBEDDING_MODELS)}"
            )
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query])[0]


def create_embedding_service(
    provider: str,
    model_name: str,
    api_key: str | None = None,
):
    if provider == "local":
        return LocalEmbeddingService(model_name=model_name)
    if provider == "openai":
        return OpenAIEmbeddingService(model=model_name, api_key=api_key)
    raise ValueError(f"Unsupported embedding provider: {provider}")