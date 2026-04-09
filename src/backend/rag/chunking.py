from __future__ import annotations

import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_markdown_into_sections(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []

    current_title = "Introduction"
    current_lines: list[str] = []

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if current_lines:
                sections.append(
                    {
                        "title": current_title,
                        "content": "\n".join(current_lines).strip(),
                    }
                )
            current_title = re.sub(r"^#{1,6}\s+", "", line).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "title": current_title,
                "content": "\n".join(current_lines).strip(),
            }
        )

    return sections

def build_documents_from_sections(
    sections: list[dict[str, str]],
    source_name: str = "handbook.md",
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    documents: list[Document] = []

    for section_index, section in enumerate(sections):
        title = section.get("title", "Untitled")
        content = section.get("content", "").strip()

        if not content:
            continue

        chunks = splitter.split_text(content)

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"{source_name}-section-{section_index}-chunk-{chunk_index}"

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source_name,
                        "section": title,
                        "section_index": section_index,
                        "chunk_index": chunk_index,
                        "chunk_id": chunk_id,
                        "approved_source": True,
                    },
                )
            )

    return documents

def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunked_docs: list[Document] = []

    for page_index, doc in enumerate(documents):
        page = doc.metadata.get("page", page_index)
        source = doc.metadata.get("source", "handbook.pdf")

        chunks = splitter.split_text(doc.page_content)

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"{source}-page-{page}-chunk-{chunk_index}"

            chunked_docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": source,
                        "page": page,
                        "chunk_index": chunk_index,
                        "chunk_id": chunk_id,
                        "approved_source": True,
                    },
                )
            )

    return chunked_docs