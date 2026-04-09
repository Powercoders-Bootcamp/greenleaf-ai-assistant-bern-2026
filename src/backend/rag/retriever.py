from __future__ import annotations

from .vector_store import get_vector_store


class HandbookRetriever:
    def __init__(
        self,
        persist_directory: str | None = None,
        embedding_model: str | None = None,
    ):
        self.db = get_vector_store(persist_directory, embedding_model)

    def retrieve(
        self,
        query: str,
        category: str | None = None,
        keywords: list[str] | None = None,
        k: int = 4,
    ) -> list[dict[str, object]]:
        enhanced_query = query
        if keywords:
            enhanced_query += " " + " ".join(keywords)

        if category:
            where_filter = {
                "$and": [
                    {"approved_source": True},
                    {"topic": category},
                ]
            }
        else:
            where_filter = {"approved_source": True}

        docs = self.db.similarity_search(
            enhanced_query,
            k=k,
            filter=where_filter,
        )

        return [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in docs
        ]