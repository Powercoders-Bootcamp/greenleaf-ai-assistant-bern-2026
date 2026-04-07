from __future__ import annotations

from embeddings import LocalEmbeddingService, OpenAIEmbeddingService


def create_embedding_service(
    provider: str,
    model_name: str,
    api_key: str | None = None,
    base_url: str | None = None,
):
    if provider == "local":
        return LocalEmbeddingService(model_name=model_name)

    if provider == "openai":
        return OpenAIEmbeddingService(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
        )

    raise ValueError(f"Unsupported embedding provider: {provider}")