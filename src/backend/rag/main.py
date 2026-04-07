from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from config import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_MAX_WORDS,
    DEFAULT_MIN_CHUNK_WORDS,
    DEFAULT_OVERLAP_WORDS,
    DEFAULT_PERSIST_DIR,
)
from ingestion_service import HandbookIngestionService
from retrieval_service import HandbookRetrievalService
from schemas import ChunkingConfig


LOCAL_MODELS = [
    "all-MiniLM-L6-v2",
    "all-mpnet-base-v2",
    "multi-qa-MiniLM-L6-cos-v1",
]

OPENAI_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]


def validate_embedding_args(provider: str, model: str) -> None:
    if provider == "local" and model not in LOCAL_MODELS:
        raise ValueError(
            f"Invalid local model: {model}. "
            f"Use one of: {LOCAL_MODELS}"
        )

    if provider == "openai" and model not in OPENAI_MODELS:
        raise ValueError(
            f"Invalid OpenAI model: {model}. "
            f"Use one of: {OPENAI_MODELS}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PDF handbook ingestion and retrieval.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Ingest handbook PDF into ChromaDB")
    ingest_parser.add_argument("--pdf-path", required=True, help="Path to the handbook PDF")
    ingest_parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR)
    ingest_parser.add_argument("--collection", default=DEFAULT_COLLECTION_NAME)
    ingest_parser.add_argument(
        "--embedding-provider",
        default="local",
        choices=["local", "openai"],
    )
    ingest_parser.add_argument(
        "--embedding-model",
        default="all-MiniLM-L6-v2",
        help="Embedding model (local or OpenAI)",
    )
    ingest_parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS)
    ingest_parser.add_argument("--overlap-words", type=int, default=DEFAULT_OVERLAP_WORDS)
    ingest_parser.add_argument("--min-chunk-words", type=int, default=DEFAULT_MIN_CHUNK_WORDS)
    ingest_parser.add_argument("--reset-collection", action="store_true")

    query_parser = subparsers.add_parser("query", help="Query the handbook vector store")
    query_parser.add_argument("--query", required=True, help="User query")
    query_parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR)
    query_parser.add_argument("--collection", default=DEFAULT_COLLECTION_NAME)
    query_parser.add_argument(
        "--embedding-provider",
        default="local",
        choices=["local", "openai"],
    )
    query_parser.add_argument(
        "--embedding-model",
        default="all-MiniLM-L6-v2",
        help="Embedding model (local or OpenAI)",
    )
    query_parser.add_argument("--top-k", type=int, default=5)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    validate_embedding_args(args.embedding_provider, args.embedding_model)

    if args.command == "ingest":
        service = HandbookIngestionService(
            embedding_provider=args.embedding_provider,
            embedding_model=args.embedding_model,
            persist_directory=args.persist_dir,
            collection_name=args.collection,
            chunking_config=ChunkingConfig(
                max_words=args.max_words,
                overlap_words=args.overlap_words,
                min_chunk_words=args.min_chunk_words,
            ),
        )
        result = service.ingest_pdf(args.pdf_path, reset_collection=args.reset_collection)
        print(json.dumps(asdict(result), indent=2))
        return

    if args.command == "query":
        service = HandbookRetrievalService(
            embedding_provider=args.embedding_provider,
            embedding_model=args.embedding_model,
            persist_directory=args.persist_dir,
            collection_name=args.collection,
        )
        result = service.query(args.query, top_k=args.top_k)
        print(json.dumps(result, indent=2))
        return


if __name__ == "__main__":
    main()