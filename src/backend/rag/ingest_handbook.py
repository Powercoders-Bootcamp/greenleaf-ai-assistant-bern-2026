from __future__ import annotations

import argparse
import json
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from .chunking import (
    build_documents_from_sections,
    chunk_documents,
    split_markdown_into_sections,
)
from .vector_store import add_documents, reset_vector_store


class HandbookIngestionService:
    def __init__(
        self,
        persist_directory: str | None = None,
        embedding_model: str | None = None,
    ):
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model

    def ingest_markdown(
        self,
        source_path: str,
        reset_collection: bool = False,
    ) -> dict[str, object]:
        file_path = Path(source_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Handbook file not found: {source_path}")

        if reset_collection:
            reset_vector_store(self.persist_directory)

        text = file_path.read_text(encoding="utf-8")
        sections = split_markdown_into_sections(text)
        documents = build_documents_from_sections(
            sections,
            source_name=file_path.name,
        )
        result = add_documents(
            documents,
            self.persist_directory,
            self.embedding_model,
        )

        return {
            "source_path": str(file_path),
            "sections_found": len(sections),
            "chunks_stored": result["chunks_stored"],
        }

    def ingest_pdf(
        self,
        source_path: str,
        reset_collection: bool = False,
    ) -> dict[str, object]:
        file_path = Path(source_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Handbook file not found: {source_path}")

        if reset_collection:
            reset_vector_store(self.persist_directory)

        loader = PyPDFLoader(str(file_path))
        documents = loader.load()
        chunked_docs = chunk_documents(documents)

        result = add_documents(
            chunked_docs,
            self.persist_directory,
            self.embedding_model,
        )

        return {
            "source_path": str(file_path),
            "pages": len(documents),
            "chunks_stored": result["chunks_stored"],
        }


def ingest_handbook_pdf(
    source_path: str,
    reset_collection: bool = False,
) -> dict[str, object]:
    service = HandbookIngestionService()
    return service.ingest_pdf(source_path, reset_collection=reset_collection)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest handbook content into ChromaDB."
    )
    parser.add_argument("source_path", help="Path to the handbook file")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and recreate the collection before ingesting",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Treat input as PDF",
    )
    args = parser.parse_args()

    service = HandbookIngestionService()

    if args.pdf:
        result = service.ingest_pdf(
            args.source_path,
            reset_collection=args.reset,
        )
    else:
        result = service.ingest_markdown(
            args.source_path,
            reset_collection=args.reset,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()