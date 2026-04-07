from __future__ import annotations

from config import DEFAULT_COLLECTION_NAME, DEFAULT_PERSIST_DIR, OPENAI_API_KEY, OPENAI_BASE_URL
from query_builder import build_keywords
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
        from embedding_factory import create_embedding_service

        self.embedder = create_embedding_service(
            provider=embedding_provider,
            model_name=embedding_model,
            api_key=openai_api_key or OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )
        self.vector_store = ChromaVectorStore(persist_directory, collection_name)

    def query(self, query_text: str, top_k: int = 5) -> dict:
        query_embedding = self.embedder.embed_query(query_text)
        return self.vector_store.query(query_embedding, top_k=top_k)

    def search_handbook(
        self,
        message: str,
        classification: str,
        top_k: int = 5,
    ) -> dict:
        keywords = build_keywords(message, classification)
        expanded_query = " ".join(keywords)

        raw_result = self.query(expanded_query, top_k=top_k)

        matches = []
        ids = raw_result.get("ids", [[]])[0]
        documents = raw_result.get("documents", [[]])[0]
        metadatas = raw_result.get("metadatas", [[]])[0]
        distances = raw_result.get("distances", [[]])[0] if "distances" in raw_result else []

        for index, chunk_id in enumerate(ids):
            metadata = metadatas[index] if index < len(metadatas) else {}
            if metadata.get("document_type") != "handbook":
                continue

            matches.append(
                {
                    "chunk_id": chunk_id,
                    "text": documents[index] if index < len(documents) else "",
                    "metadata": metadata,
                    "distance": distances[index] if index < len(distances) else None,
                }
            )

        return {
            "classification": classification,
            "keywords": keywords,
            "matches": matches,
        }