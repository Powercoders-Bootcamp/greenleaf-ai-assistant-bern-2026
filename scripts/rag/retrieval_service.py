from __future__ import annotations

from config import DEFAULT_COLLECTION_NAME, DEFAULT_PERSIST_DIR
from embedding_factory import create_embedding_service
from vector_store import ChromaVectorStore


class HandbookRetrievalService:
    def __init__(
        self,
        embedding_provider: str = "local",
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = DEFAULT_PERSIST_DIR,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        openai_api_key: str | None = None,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model

        self.embedder = create_embedding_service(
            provider=embedding_provider,
            model_name=embedding_model,
            api_key=openai_api_key,
        )
        self.vector_store = ChromaVectorStore(persist_directory, collection_name)

    def query(self, query_text: str, top_k: int = 5) -> dict:
        query_embedding = self.embedder.embed_query(query_text)
        return self.vector_store.query(query_embedding, top_k=top_k)