from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from schemas import HandbookIngestionError
from utils import TextNormalizer


class PDFHandbookLoader:
    """Loads text page by page from a PDF handbook."""

    @staticmethod
    def load_pdf(pdf_path: str | Path) -> list[dict[str, Any]]:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {path.suffix}")

        reader = PdfReader(str(path))
        pages: list[dict[str, Any]] = []

        for page_number, page in enumerate(reader.pages, start=1):
            raw_text = page.extract_text() or ""
            pages.append(
                {
                    "page_number": page_number,
                    "text": TextNormalizer.normalize(raw_text),
                }
            )

        if not any(page["text"].strip() for page in pages):
            raise HandbookIngestionError("No extractable text found in the PDF.")

        return pages
