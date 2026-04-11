#!/usr/bin/env python3
"""
Run handbook/RAG tests from a text file.

For each non-empty line in the input .txt file, the script prints and optionally
saves:
1) the original question
2) the raw RAG retrieval output from search_handbook
3) the final answer from run_chat (system prompt + tool use)

Usage examples
--------------
python query_tester.py questions.txt
python query_tester.py questions.txt --output results.txt
python query_tester.py questions.txt --show-errors
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _setup_imports() -> None:
    """
    Make imports work whether the script is placed in the repo root
    or moved elsewhere.
    """
    script_path = Path(__file__).resolve()
    candidates = [
        script_path.parent,
        script_path.parent / "src",
        script_path.parent.parent / "src",
    ]
    for candidate in candidates:
        if candidate.exists():
            sys.path.insert(0, str(candidate))


_setup_imports()

try:
    from services.langchain_service import run_chat, search_handbook
except Exception as exc:
    raise RuntimeError(
        "Could not import backend.services.langchain_service. "
        "Place this file in your project root (or adjust sys.path), then run it from there."
    ) from exc


def read_questions(txt_path: Path) -> list[str]:
    if not txt_path.exists():
        raise FileNotFoundError(f"Input file not found: {txt_path}")

    lines = txt_path.read_text(encoding="utf-8").splitlines()
    questions = [line.strip() for line in lines if line.strip()]
    if not questions:
        raise ValueError(f"No non-empty questions found in: {txt_path}")
    return questions


def get_rag_answer(question: str) -> str:
    """
    Raw retrieval result only.
    """
    return search_handbook.invoke({"query": question})


def get_prompt_answer(question: str) -> str:
    """
    Final model answer using the system prompt and tools.
    """
    return run_chat(question)


def format_result(index: int, question: str, rag_answer: str, prompt_answer: str) -> str:
    return (
        f"{'=' * 90}\n"
        f"Question {index}\n"
        f"{'=' * 90}\n"
        f"QUESTION:\n{question}\n\n"
        f"RAG ANSWER:\n{rag_answer}\n\n"
        f"PROMPT ANSWER:\n{prompt_answer}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare raw RAG output with final prompt-based answer for questions in a text file."
    )
    parser.add_argument("input_file", help="Path to a .txt file containing one question per line.")
    parser.add_argument(
        "--output",
        help="Optional path to save the full results to a text file.",
        default=None,
    )
    parser.add_argument(
        "--show-errors",
        action="store_true",
        help="Include full exception messages in output instead of a short error line.",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    questions = read_questions(input_path)
    blocks: list[str] = []

    for i, question in enumerate(questions, start=1):
        try:
            rag_answer = get_rag_answer(question)
        except Exception as exc:
            rag_answer = f"[ERROR while getting RAG answer] {exc}" if args.show_errors else "[ERROR while getting RAG answer]"

        try:
            prompt_answer = get_prompt_answer(question)
        except Exception as exc:
            prompt_answer = f"[ERROR while getting prompt answer] {exc}" if args.show_errors else "[ERROR while getting prompt answer]"

        block = format_result(i, question, rag_answer, prompt_answer)
        blocks.append(block)
        print(block)

    if output_path is not None:
        output_path.write_text("\n\n".join(blocks), encoding="utf-8")
        print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()
