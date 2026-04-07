from __future__ import annotations

from pathlib import Path

from chunker import HandbookChunker, SectionParser
from config import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_PERSIST_DIR,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
)
from embedding_factory import create_embedding_service
from loaders import PDFHandbookLoader
from schemas import ChunkingConfig, IngestionResult
from vector_store import ChromaVectorStore


class HandbookIngestionService:
    def __init__(
        self,
        embedding_provider: str = "local",
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = DEFAULT_PERSIST_DIR,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        chunking_config: ChunkingConfig | None = None,
        openai_api_key: str | None = None,
        openai_base_url: str | None = None,
    ) -> None:
        self.embedding_provider = embedding_provider
        self.embedding_model = embedding_model
        self.chunking_config = chunking_config or ChunkingConfig()

        self.loader = PDFHandbookLoader()
        self.parser = SectionParser()
        self.embedder = create_embedding_service(
            provider=embedding_provider,
            model_name=embedding_model,
            api_key=openai_api_key or OPENAI_API_KEY,
            base_url=openai_base_url or OPENAI_BASE_URL,
        )
        self.vector_store = ChromaVectorStore(persist_directory, collection_name)
        self.chunker = HandbookChunker(self.chunking_config, embedding_model)

    def ingest_pdf(self, pdf_path: str | Path, reset_collection: bool = False) -> IngestionResult:
        if reset_collection:
            self.vector_store.reset_collection()

        pages = self.loader.load_pdf(pdf_path)
        source_name = Path(pdf_path).name
        sections = self.parser.parse(pages, source=source_name)
        chunks = self.chunker.chunk_sections(sections)
        embeddings = self.embedder.embed_texts([chunk.text for chunk in chunks])
        self.vector_store.upsert_chunks(chunks, embeddings)

        return IngestionResult(
            status="success",
            source=source_name,
            sections_count=len(sections),
            chunks_count=len(chunks),
            collection=self.vector_store.collection.name,
            embedding_model=self.embedding_model,
        )