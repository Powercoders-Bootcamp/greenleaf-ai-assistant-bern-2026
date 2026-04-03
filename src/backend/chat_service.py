"""
OpenAI chat orchestration with registered tools (check_holiday, search_handbook).
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from openai import OpenAI

from holidays_checker import HolidayAPIError, is_day_a_holiday, parse_iso_date

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
TOOLS_DIR = PROMPTS_DIR / "tools_definitions"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.txt"
HANDBOOK_PATH = REPO_ROOT / "data" / "processed" / "handbook-key-rules.md"
SESSION_TIMEZONE = ZoneInfo("Europe/Zurich")

DEFAULT_MODEL = "gpt-4o"
MAX_TOOL_ROUNDS = 6


def load_system_prompt() -> str:
    text = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").rstrip()
    now = datetime.now(SESSION_TIMEZONE)
    today_suffix = (
        "\n\n---\n"
        "Today's date (for this request, Europe/Zurich): "
        f"{now.strftime('%A')}, {now:%Y-%m-%d}.\n"
    )
    return text + today_suffix


def load_tool_definitions() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for filename in ("check_holiday.json", "search_handbook.json"):
        path = TOOLS_DIR / filename
        tools.append(json.loads(path.read_text(encoding="utf-8")))
    return tools


def _run_check_holiday(arguments: dict[str, Any]) -> dict[str, Any]:
    date_raw = arguments.get("date")
    day = parse_iso_date(date_raw) if isinstance(date_raw, str) else None
    if day is None:
        return {
            "error": "Invalid or missing date. Use ISO format YYYY-MM-DD.",
            "received": date_raw,
        }
    try:
        return dict(is_day_a_holiday(day))
    except HolidayAPIError as exc:
        return {"error": str(exc)}


def _run_search_handbook(arguments: dict[str, Any]) -> str:
    raw_keywords = arguments.get("keywords")
    if not isinstance(raw_keywords, list) or not all(
        isinstance(k, str) for k in raw_keywords
    ):
        return "Invalid keywords: provide a list of strings."
    keywords_lower = [k.lower() for k in raw_keywords if k.strip()]
    if not keywords_lower:
        return "No keywords provided."

    if not HANDBOOK_PATH.is_file():
        return "Handbook file is not available on the server."

    lines = HANDBOOK_PATH.read_text(encoding="utf-8").splitlines()
    hits: list[str] = []
    for line in lines:
        low = line.lower()
        if any(k in low for k in keywords_lower):
            hits.append(line)
    if not hits:
        return "No matching sections found for the given keywords."
    text = "\n".join(hits[:80])
    return text[:8000]


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    if name == "check_holiday":
        payload = _run_check_holiday(arguments)
        return json.dumps(payload, ensure_ascii=False)
    if name == "search_handbook":
        return _run_search_handbook(arguments)
    return json.dumps({"error": f"Unknown tool: {name}"})


def _append_assistant_message(messages: list[dict[str, Any]], assistant_msg: Any) -> None:
    entry: dict[str, Any] = {"role": "assistant", "content": assistant_msg.content}
    if assistant_msg.tool_calls:
        entry["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in assistant_msg.tool_calls
        ]
    messages.append(entry)


def run_chat(user_message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    client = OpenAI(api_key=api_key)
    tools = load_tool_definitions()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": load_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        choice = response.choices[0]
        assistant_msg = choice.message

        if assistant_msg.tool_calls:
            _append_assistant_message(messages, assistant_msg)
            for tc in assistant_msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                result = execute_tool(tc.function.name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    }
                )
            continue

        text = (assistant_msg.content or "").strip()
        if text:
            return text
        return "The model returned an empty response."

    return "Tool loop limit reached; please try a simpler question."
