"""
PII masking with regex + spaCy NER.

This script detects and masks personally identifiable information (PII)
in English text.

What this script does:
1. Detects structured sensitive data with regex
2. Detects named entities with spaCy
3. Merges and filters matches without overlaps
4. Replaces detected values with placeholders like
   [EMAIL], [PERSON], [ORG], [LOCATION]

Required dependencies:
- Python 3.10+
- spaCy
- spaCy English model: en_core_web_sm

Setup:
    pip install --upgrade pip
    pip install spacy
    python -m spacy download en_core_web_sm

Run:
    python pii_masker.py

Usage as a black-box module:
- Main entry point: mask_pii(text: str) -> str
- Input must be a string
- Output is a masked string
- If input is invalid, an exception is raised
- The function does not return unmasked input on validation failure
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

try:
    import spacy
except ImportError:  # pragma: no cover - depends on local optional setup
    spacy = None


try:
    nlp = spacy.load("en_core_web_sm") if spacy is not None else None
except OSError:  # pragma: no cover - depends on local optional setup
    nlp = None


REGEX_PATTERNS: dict[str, str] = {
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "PHONE": r"""(?x)
        (?<!\w)
        (?:\+?\d{1,3}[\s\-().]*)?
        (?:\(?\d{2,4}\)?[\s\-().]*)?
        \d{3,4}[\s\-().]*\d{3,4}
        (?!\w)
    """,
    "URL": r"\bhttps?://[^\s]+|\bwww\.[^\s]+\b",
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "MAC": r"\b(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,19}\b",
    "ID": r"\b(?:ID[:\s-]*)?[A-Z0-9]{6,20}\b",
    "SSN": r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",
}

NER_LABEL_MAP: dict[str, str] = {
    "PERSON": "PERSON",
    "ORG": "ORG",
    "GPE": "LOCATION",
    "LOC": "LOCATION",
    "FAC": "LOCATION",
    "DATE": "DATE",
    "TIME": "TIME",
}


@dataclass(frozen=True)
class Match:
    start: int
    end: int
    label: str

    @property
    def length(self) -> int:
        return self.end - self.start

    def placeholder(self) -> str:
        return f"[{self.label}]"

def is_valid_span(start: int, end: int, text_length: int) -> bool:
    """
    Validate match boundaries.
    """
    return 0 <= start < end <= text_length


def collect_regex_matches(text: str) -> list[Match]:
    """
    Detect structured PII using regex patterns.
    """
    matches: list[Match] = []

    for label, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            candidate = Match(match.start(), match.end(), label)
            if is_valid_span(candidate.start, candidate.end, len(text)):
                matches.append(candidate)

    return matches


def collect_ner_matches(text: str, include_temporal: bool = False) -> list[Match]:
    """
    Detect entities using spaCy NER.
    """
    if nlp is None:
        return []

    matches: list[Match] = []
    doc = nlp(text)

    for ent in doc.ents:
        mapped_label = NER_LABEL_MAP.get(ent.label_)
        if not mapped_label:
            continue
        if not include_temporal and mapped_label in {"DATE", "TIME"}:
            continue

        candidate = Match(ent.start_char, ent.end_char, mapped_label)
        if is_valid_span(candidate.start, candidate.end, len(text)):
            matches.append(candidate)

    return matches


def sort_matches(matches: Iterable[Match]) -> list[Match]:
    """
    Sort by longer span first, then by earlier start position.
    This helps resolve overlaps more reliably.
    """
    return sorted(matches, key=lambda m: (-m.length, m.start))


def select_non_overlapping_matches(matches: list[Match], text_length: int) -> list[Match]:
    """
    Keep only non-overlapping matches.
    Longer matches are preferred because input is pre-sorted.
    """
    occupied = [False] * text_length
    selected: list[Match] = []

    for match in matches:
        if any(occupied[match.start:match.end]):
            continue

        selected.append(match)
        for i in range(match.start, match.end):
            occupied[i] = True

    return selected


def replace_matches(text: str, matches: list[Match]) -> str:
    """
    Replace matches from right to left to preserve offsets.
    """
    result = text

    for match in sorted(matches, key=lambda m: m.start, reverse=True):
        result = result[:match.start] + match.placeholder() + result[match.end:]

    return result


def mask_pii(text: str, include_temporal: bool = False) -> str:
    """
    Main pipeline:
    1. Validate input
    2. Collect regex matches
    3. Collect NER matches
    4. Resolve overlaps
    5. Replace with placeholders
    """
    if not isinstance(text, str):
        raise TypeError("mask_pii expects a string")
    if not text:
        raise ValueError("mask_pii received empty text")

    regex_matches = collect_regex_matches(text)
    ner_matches = collect_ner_matches(text, include_temporal=include_temporal)

    all_matches = regex_matches + ner_matches
    ordered_matches = sort_matches(all_matches)
    selected_matches = select_non_overlapping_matches(ordered_matches, len(text))

    return replace_matches(text, selected_matches)


if __name__ == "__main__":
    test_text = """
    John Smith lives in London.
    He works at Google since 2022.
    Contact him at john.smith@gmail.com or +44 7700 900123.
    His ID is ABX992211 and server IP is 192.168.1.1.
    Website: https://example.com
    """

    print("=== ORIGINAL ===")
    print(test_text)

    print("\n=== ANONYMIZED ===")
    print(mask_pii(test_text))
