from embeddings import OpenAIEmbeddingService
from embeddings import LocalEmbeddingService

def create_embedding_service(provider: str, model_name: str, api_key: str | None = None):
    if provider == "openai":
        return OpenAIEmbeddingService(model=model_name, api_key=api_key)
    if provider == "local":
        return LocalEmbeddingService(model_name=model_name)
    raise ValueError(f"Unsupported embedding provider: {provider}")