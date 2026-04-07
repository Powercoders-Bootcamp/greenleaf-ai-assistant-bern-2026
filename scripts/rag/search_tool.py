from __future__ import annotations

from retrieval_service import HandbookRetrievalService


class HandbookSearchTool:
    def __init__(self, retrieval_service: HandbookRetrievalService) -> None:
        self.retrieval_service = retrieval_service

    def search_handbook(
        self,
        message: str,
        classification: str,
        top_k: int = 5,
    ) -> dict:
        return self.retrieval_service.search_handbook(
            message=message,
            classification=classification,
            top_k=top_k,
        )