from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config import DEFAULT_DOCUMENT_TYPE


class HandbookIngestionError(Exception):
    """Raised when handbook ingestion fails."""


@dataclass(slots=True)
class ChunkingConfig:
    max_words: int = 220
    overlap_words: int = 40
    min_chunk_words: int = 30

    def __post_init__(self) -> None:
        if self.max_words <= 0:
            raise ValueError("max_words must be > 0")
        if self.overlap_words < 0:
            raise ValueError("overlap_words must be >= 0")
        if self.overlap_words >= self.max_words:
            raise ValueError("overlap_words must be smaller than max_words")
        if self.min_chunk_words <= 0:
            raise ValueError("min_chunk_words must be > 0")


@dataclass(slots=True)
class Section:
    number: str
    title: str
    body: str
    source: str
    pages: list[int]


@dataclass(slots=True)
class DocumentChunk:
    chunk_id: str
    text: str
    source: str
    section_number: str
    section_title: str
    chunk_index: int
    page_start: int | None
    page_end: int | None
    word_count: int
    char_count: int
    embedding_model: str
    document_type: str = DEFAULT_DOCUMENT_TYPE

    def metadata(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "section_number": self.section_number,
            "section_title": self.section_title,
            "chunk_index": self.chunk_index,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "embedding_model": self.embedding_model,
            "document_type": self.document_type,
        }


@dataclass(slots=True)
class IngestionResult:
    status: str
    source: str
    sections_count: int
    chunks_count: int
    collection: str
    embedding_model: str
