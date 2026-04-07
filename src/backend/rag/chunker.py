from __future__ import annotations

import hashlib
import re
from typing import Iterable

from schemas import ChunkingConfig, DocumentChunk, Section
from utils import TextNormalizer


class SectionParser:
    """Parses major numbered sections from handbook text."""

    SECTION_PATTERN = re.compile(r"(?m)^\s*(\d+)\.\s+([A-Z][A-Z\s&\-,()'/]+)\s*$")

    def parse(self, pages: list[dict], source: str) -> list[Section]:
        full_text_parts: list[str] = []
        page_markers: list[tuple[int, int, int]] = []
        cursor = 0

        for page in pages:
            page_text = page["text"]
            full_text_parts.append(page_text)
            start = cursor
            cursor += len(page_text)
            end = cursor
            page_markers.append((page["page_number"], start, end))
            full_text_parts.append("\n\n")
            cursor += 2

        full_text = "".join(full_text_parts).strip()
        matches = list(self.SECTION_PATTERN.finditer(full_text))
        if not matches:
            raise ValueError("No numbered sections were detected in the handbook.")

        sections: list[Section] = []
        for index, match in enumerate(matches):
            content_start = match.end()
            content_end = matches[index + 1].start() if index + 1 < len(matches) else len(full_text)
            sections.append(
                Section(
                    number=match.group(1).strip(),
                    title=match.group(2).strip(),
                    body=full_text[content_start:content_end].strip(),
                    source=source,
                    pages=self._find_pages_for_range(content_start, content_end, page_markers),
                )
            )
        return sections

    @staticmethod
    def _find_pages_for_range(
        range_start: int,
        range_end: int,
        page_markers: list[tuple[int, int, int]],
    ) -> list[int]:
        pages: list[int] = []
        for page_number, start, end in page_markers:
            overlaps = not (range_end < start or range_start > end)
            if overlaps:
                pages.append(page_number)
        return pages


class HandbookChunker:
    """Section-aware chunker with paragraph and sentence fallback."""

    def __init__(self, config: ChunkingConfig, embedding_model: str) -> None:
        self.config = config
        self.embedding_model = embedding_model

    def chunk_sections(self, sections: Iterable[Section]) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        for section in sections:
            chunks.extend(self._chunk_one_section(section))
        return chunks

    def _chunk_one_section(self, section: Section) -> list[DocumentChunk]:
        text = TextNormalizer.normalize(section.body)
        if not text:
            return []

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()] or [text]
        current_parts: list[str] = []
        current_words = 0
        chunk_texts: list[str] = []

        for paragraph in paragraphs:
            paragraph_word_count = self._word_count(paragraph)

            if paragraph_word_count > self.config.max_words:
                for sentence_piece in self._split_large_paragraph(paragraph):
                    piece_words = self._word_count(sentence_piece)
                    if current_words + piece_words <= self.config.max_words:
                        current_parts.append(sentence_piece)
                        current_words += piece_words
                    else:
                        if current_parts:
                            chunk_texts.append("\n\n".join(current_parts).strip())
                        overlap = self._tail_words("\n\n".join(current_parts), self.config.overlap_words)
                        current_parts = [overlap, sentence_piece] if overlap else [sentence_piece]
                        current_words = self._word_count(" ".join(current_parts))
                continue

            if current_words + paragraph_word_count <= self.config.max_words:
                current_parts.append(paragraph)
                current_words += paragraph_word_count
            else:
                if current_parts:
                    chunk_texts.append("\n\n".join(current_parts).strip())
                overlap = self._tail_words("\n\n".join(current_parts), self.config.overlap_words)
                current_parts = [overlap, paragraph] if overlap else [paragraph]
                current_words = self._word_count(" ".join(current_parts))

        if current_parts:
            final_chunk = "\n\n".join(part for part in current_parts if part.strip()).strip()
            if final_chunk:
                chunk_texts.append(final_chunk)

        chunk_texts = self._merge_small_trailing_chunks(chunk_texts)
        page_start = min(section.pages) if section.pages else None
        page_end = max(section.pages) if section.pages else None

        return [
            DocumentChunk(
                chunk_id=self._build_chunk_id(section.source, section.number, chunk_index, chunk_text),
                text=chunk_text,
                source=section.source,
                section_number=section.number,
                section_title=section.title,
                chunk_index=chunk_index,
                page_start=page_start,
                page_end=page_end,
                word_count=self._word_count(chunk_text),
                char_count=len(chunk_text),
                embedding_model=self.embedding_model,
            )
            for chunk_index, chunk_text in enumerate(chunk_texts)
        ]

    def _split_large_paragraph(self, paragraph: str) -> list[str]:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\-\(\"])", paragraph)
            if sentence.strip()
        ] or [paragraph]

        pieces: list[str] = []
        for sentence in sentences:
            if self._word_count(sentence) <= self.config.max_words:
                pieces.append(sentence)
                continue

            words = sentence.split()
            step = max(1, self.config.max_words - self.config.overlap_words)
            for index in range(0, len(words), step):
                pieces.append(" ".join(words[index:index + self.config.max_words]).strip())
        return pieces

    def _merge_small_trailing_chunks(self, chunks: list[str]) -> list[str]:
        merged: list[str] = []
        for chunk in chunks:
            if merged and self._word_count(chunk) < self.config.min_chunk_words:
                merged[-1] = (merged[-1] + "\n\n" + chunk).strip()
            else:
                merged.append(chunk)
        return merged

    @staticmethod
    def _word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def _tail_words(text: str, count: int) -> str:
        words = text.split()
        return " ".join(words[-count:]) if words else ""

    @staticmethod
    def _build_chunk_id(source: str, section_number: str, chunk_index: int, text: str) -> str:
        digest = hashlib.sha256(
            f"{source}:{section_number}:{chunk_index}:{text}".encode("utf-8")
        ).hexdigest()[:16]
        source_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", source)
        return f"{source_slug}_sec{section_number}_chunk{chunk_index}_{digest}"
