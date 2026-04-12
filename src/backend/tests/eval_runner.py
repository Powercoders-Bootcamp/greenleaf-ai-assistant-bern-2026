from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Callable

CURRENT_FILE = Path(__file__).resolve()
SRC_ROOT = CURRENT_FILE.parents[2]  # /app/src
RUN_TIMEZONE = ZoneInfo("Europe/Zurich")

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def resolve_backend_root() -> Path:
    return CURRENT_FILE.parents[1]


BACKEND_ROOT = resolve_backend_root()
TESTS_DIR = BACKEND_ROOT / "tests"
FIXTURES_DIR = TESTS_DIR / "fixtures"
ARTIFACTS_DIR = TESTS_DIR / "artifacts"


def import_run_chat():
    """
    Import run_chat lazily so that import errors are easier to understand
    and the script fails with a clear message.
    """
    try:
        from backend.services.langchain_service import run_chat
        return run_chat
    except Exception as exc:
        raise RuntimeError(
            "Could not import run_chat from "
            "backend.services.langchain_service. "
            "Make sure the import path is correct and that /app/src is available "
            "on PYTHONPATH."
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch evaluation runner for chat orchestration."
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--file",
        type=str,
        help="Run a single CSV file from tests/fixtures, for example: smoke.csv",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Run all CSV files from tests/fixtures.",
    )

    return parser.parse_args()


def ensure_directories() -> None:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def discover_fixture_files(file_name: str | None) -> list[Path]:
    if file_name:
        path = FIXTURES_DIR / file_name
        if not path.is_file():
            raise FileNotFoundError(f"Fixture file not found: {path}")
        return [path]

    files = sorted(FIXTURES_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(
            f"No CSV fixture files were found in directory: {FIXTURES_DIR}"
        )
    return files


def create_run_directory() -> Path:
    timestamp = datetime.now(RUN_TIMEZONE).strftime("run_%Y-%m-%d_%H-%M-%S")
    run_dir = ARTIFACTS_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        expected_columns = {"id", "history", "question"}
        actual_columns = set(reader.fieldnames or [])

        missing = expected_columns - actual_columns
        if missing:
            raise ValueError(
                f"File {csv_path.name} is missing required columns: "
                f"{', '.join(sorted(missing))}"
            )

        return list(reader)


def parse_history(
    raw: str | None,
    row_id: str,
    file_name: str,
) -> list[dict[str, str]] | None:
    value = (raw or "").strip()
    if not value:
        return None

    try:
        data = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"[{file_name} | id={row_id}] 'history' is not valid JSON: {exc}"
        ) from exc

    if not isinstance(data, list):
        raise ValueError(
            f"[{file_name} | id={row_id}] 'history' must be a JSON array."
        )

    normalized: list[dict[str, str]] = []

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(
                f"[{file_name} | id={row_id}] history[{index}] must be an object."
            )

        role = item.get("role")
        content = item.get("content")

        if role not in {"user", "assistant"}:
            raise ValueError(
                f"[{file_name} | id={row_id}] history[{index}].role "
                f"must be either 'user' or 'assistant'."
            )

        if not isinstance(content, str):
            raise ValueError(
                f"[{file_name} | id={row_id}] history[{index}].content "
                f"must be a string."
            )

        normalized.append({"role": role, "content": content})

    return normalized


def write_output_csv(output_path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["id", "history", "question", "answer"]

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_fixture(
    csv_path: Path,
    output_dir: Path,
    run_chat_func: Callable,
) -> tuple[int, int]:
    input_rows = load_rows(csv_path)
    output_rows: list[dict[str, str]] = []

    success_count = 0
    error_count = 0

    for row in input_rows:
        row_id = (row.get("id") or "").strip()
        history_raw = row.get("history") or ""
        question = (row.get("question") or "").strip()

        if not row_id:
            error_count += 1
            output_rows.append(
                {
                    "id": "",
                    "history": history_raw,
                    "question": question,
                    "answer": "ERROR: missing id",
                }
            )
            continue

        if not question:
            error_count += 1
            output_rows.append(
                {
                    "id": row_id,
                    "history": history_raw,
                    "question": "",
                    "answer": "ERROR: empty question",
                }
            )
            continue

        try:
            parsed_history = parse_history(
                history_raw,
                row_id=row_id,
                file_name=csv_path.name,
            )

            answer = run_chat_func(
                user_message=question,
                conversation_messages=parsed_history,
            )

            if not isinstance(answer, str):
                answer = str(answer)

            output_rows.append(
                {
                    "id": row_id,
                    "history": history_raw,
                    "question": question,
                    "answer": answer,
                }
            )
            success_count += 1

        except Exception as exc:
            output_rows.append(
                {
                    "id": row_id,
                    "history": history_raw,
                    "question": question,
                    "answer": f"ERROR: {exc}",
                }
            )
            error_count += 1

    output_path = output_dir / csv_path.name
    write_output_csv(output_path, output_rows)
    return success_count, error_count


def main() -> int:
    args = parse_args()
    ensure_directories()

    run_chat_func = import_run_chat()

    fixture_files = discover_fixture_files(file_name=args.file)

    run_dir = create_run_directory()

    total_success = 0
    total_errors = 0

    print(f"Input fixtures directory: {FIXTURES_DIR}")
    print(f"Artifacts run directory:  {run_dir}")
    print()

    for csv_path in fixture_files:
        print(f"Running fixture: {csv_path.name}")
        success_count, error_count = run_fixture(
            csv_path=csv_path,
            output_dir=run_dir,
            run_chat_func=run_chat_func,
        )
        total_success += success_count
        total_errors += error_count
        print(
            f"Finished fixture: {csv_path.name} | "
            f"success={success_count} | errors={error_count}"
        )

    print()
    print(f"Done. Total success={total_success}, total errors={total_errors}")
    print(f"Results saved in: {run_dir}")

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())