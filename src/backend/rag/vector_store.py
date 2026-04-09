from __future__ import annotations

import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .config import COLLECTION_NAME, VECTOR_DB_DIR
from .embeddings import get_embeddings


def reset_vector_store(persist_directory: str | Path | None = None) -> None:
    target = Path(persist_directory or VECTOR_DB_DIR)
    if target.exists():
        shutil.rmtree(target)


def get_vector_store(persist_directory: str | Path | None = None, embedding_model: str | None = None) -> Chroma:
    target = Path(persist_directory or VECTOR_DB_DIR)
    target.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(target),
        embedding_function=get_embeddings(embedding_model),
    )


def add_documents(
    documents: list[Document],
    persist_directory: str | Path | None = None,
    embedding_model: str | None = None,
) -> dict[str, int]:
    db = get_vector_store(persist_directory, embedding_model)
    ids = [str(doc.metadata["chunk_id"]) for doc in documents]
    db.add_documents(documents=documents, ids=ids)
    return {"chunks_stored": len(documents)}
