"""
LangChain-based chat orchestration with:
- tool calling
- FAISS-backed handbook retrieval
- holiday checking tool

Dependencies
------------
Install the required packages:

    pip install -U langchain langchain-openai langchain-community langchain-text-splitters faiss-cpu openai python-dotenv
Optional but useful for tracing/debugging:
    pip install -U langsmith

Environment variables
---------------------
Required:
    OPENAI_API_KEY=...

Notes
-----
1. This module builds the FAISS index on first run if it does not exist yet.
2. The FAISS index is stored on disk and reused on subsequent runs.
3. The handbook search is semantic (embeddings + vector search), not plain keyword matching.
4. `check_holiday` remains a deterministic Python tool.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from .holidays_checker import HolidayAPIError, is_day_a_holiday, parse_iso_date

from pathlib import Path
import os

SERVICE_FILE = Path(__file__).resolve()

REPO_ROOT = SERVICE_FILE.parents[3]
SRC_ROOT = REPO_ROOT / "src"
BACKEND_ROOT = SRC_ROOT / "backend"
SERVICES_ROOT = BACKEND_ROOT / "services"

PROMPTS_DIR = REPO_ROOT / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system_prompt.txt"

HANDBOOK_RAW_PATH = REPO_ROOT / "data" / "raw" / "Handbook GreenLeaf Logistics.pdf"
HANDBOOK_PATH = REPO_ROOT / "data" / "processed" / "handbook-structured.md"

FAISS_DIR = Path(
    os.getenv(
        "HANDBOOK_FAISS_DIR",
        str(REPO_ROOT / "data" / "vectorstore" / "handbook_faiss"),
    )
)

SESSION_TIMEZONE = ZoneInfo("Europe/Zurich")

DEFAULT_MODEL = "gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
MAX_TOOL_ROUNDS = 6


load_dotenv()

def load_system_prompt() -> str:
    text = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").rstrip()
    now = datetime.now(SESSION_TIMEZONE)
    today_suffix = (
        "\n\n---\n"
        "Today's date (for this request, Europe/Zurich): "
        f"{now.strftime('%A')}, {now:%Y-%m-%d}.\n"
    )
    return text + today_suffix


def _stringify_content(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part).strip()
    return str(content).strip()


def _load_handbook_text() -> str:
    if not HANDBOOK_PATH.is_file():
        raise FileNotFoundError(f"Handbook file not found: {HANDBOOK_PATH}")
    return HANDBOOK_PATH.read_text(encoding="utf-8")


def _split_handbook_into_documents(text: str) -> list[Document]:
    chunk_size = int(os.getenv("HANDBOOK_CHUNK_SIZE", "350"))
    chunk_overlap = int(os.getenv("HANDBOOK_CHUNK_OVERLAP", "50"))

    headers_to_split_on = [
        ("##", "section"),
        ("###", "subsection"),
        ("####", "subsubsection"),
    ]

    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )

    section_docs = md_splitter.split_text(text)

    secondary_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    split_docs = secondary_splitter.split_documents(section_docs)

    documents: list[Document] = []

    for idx, doc in enumerate(split_docs):
        cleaned = doc.page_content.strip()
        if not cleaned:
            continue

        metadata = dict(doc.metadata or {})
        metadata.update(
            {
                "source": str(HANDBOOK_PATH),
                "document_name": HANDBOOK_PATH.name,
                "chunk_id": idx,
            }
        )

        documents.append(
            Document(
                page_content=cleaned,
                metadata=metadata,
            )
        )

    return documents


def _build_vectorstore(embeddings: OpenAIEmbeddings) -> FAISS:
    text = _load_handbook_text()
    documents = _split_handbook_into_documents(text)
    vectorstore = FAISS.from_documents(documents, embeddings)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(FAISS_DIR))
    return vectorstore


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    base_url = os.getenv("OPENAI_BASE_URL")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)

    kwargs: dict[str, Any] = {
        "model": embedding_model,
        "api_key": api_key,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return OpenAIEmbeddings(**kwargs)


@lru_cache(maxsize=1)
def get_vectorstore() -> FAISS:
    embeddings = get_embeddings()

    index_file = FAISS_DIR / "index.faiss"
    pkl_file = FAISS_DIR / "index.pkl"

    if index_file.exists() and pkl_file.exists():
        return FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    return _build_vectorstore(embeddings)


@lru_cache(maxsize=1)
def get_retriever():
    k = int(os.getenv("HANDBOOK_RETRIEVAL_K", "6"))
    return get_vectorstore().as_retriever(search_kwargs={"k": k})


@tool
def check_holiday(date: str) -> str:
    """
    Check whether the given ISO date (YYYY-MM-DD) is a holiday.
    """
    day = parse_iso_date(date) if isinstance(date, str) else None
    if day is None:
        return json.dumps(
            {
                "error": "Invalid or missing date. Use ISO format YYYY-MM-DD.",
                "received": date,
            },
            ensure_ascii=False,
        )

    try:
        payload = dict(is_day_a_holiday(day))
        return json.dumps(payload, ensure_ascii=False)
    except HolidayAPIError as exc:
        return json.dumps({"error": str(exc)}, ensure_ascii=False)


def _format_docs_for_llm(docs: list[Document]) -> str:
    if not docs:
        return "No relevant handbook sections were found."

    parts: list[str] = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("document_name", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "?")
        section = doc.metadata.get("section", "")
        subsection = doc.metadata.get("subsection", "")

        header = (
            f"[Handbook excerpt {i} | source={source} | chunk_id={chunk_id}"
            f" | section={section or '-'} | subsection={subsection or '-'}]"
        )

        parts.append(f"{header}\n{doc.page_content}")

    return "\n\n".join(parts)


@tool
def search_handbook(query: str) -> str:
    """
    Search the employee handbook semantically and return the most relevant excerpts.
    """
    if not isinstance(query, str) or not query.strip():
        return "Invalid query: provide a non-empty string."

    docs = get_retriever().invoke(query)
    return _format_docs_for_llm(docs)


def get_llm() -> ChatOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    base_url = os.getenv("OPENAI_BASE_URL")

    kwargs: dict[str, Any] = {
        "model": model,
        "api_key": api_key,
        "temperature": 0,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)

def _convert_history(conversation_messages: list[dict[str, str]]) -> list[Any]:
    result = []

    for msg in conversation_messages:
        role = msg.get("role")
        content = msg.get("content", "")

        if role == "user":
            result.append(HumanMessage(content=content))
        elif role == "assistant":
            result.append(AIMessage(content=content))
        # system можна додати за потреби

    return result

def run_chat(user_message: str,
             conversation_messages: list[dict[str, str]] | None = None,
             ) -> str:
    llm = get_llm()
    tools = [check_holiday, search_handbook]
    llm_with_tools = llm.bind_tools(tools)

    tool_registry = {tool.name: tool for tool in tools}

    messages: list[Any] = [
        SystemMessage(content=load_system_prompt()),
    ]

    if conversation_messages:
        messages.extend(_convert_history(conversation_messages))

    messages.append(HumanMessage(content=user_message))

    for _ in range(MAX_TOOL_ROUNDS):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        tool_calls = getattr(ai_msg, "tool_calls", None) or []
        if not tool_calls:
            text = _stringify_content(ai_msg.content)
            return text or "The model returned an empty response."

        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call.get("args", {})
            tool_call_id = call["id"]

            selected_tool = tool_registry.get(tool_name)
            if selected_tool is None:
                tool_result = json.dumps(
                    {"error": f"Unknown tool: {tool_name}"},
                    ensure_ascii=False,
                )
            else:
                try:
                    # LangChain tools accept dict input for structured args
                    tool_result = selected_tool.invoke(tool_args)
                except Exception as exc:  # defensive: keep the loop alive
                    tool_result = json.dumps(
                        {"error": f"Tool execution failed: {exc}"},
                        ensure_ascii=False,
                    )

            messages.append(
                ToolMessage(
                    content=_stringify_content(tool_result),
                    tool_call_id=tool_call_id,
                )
            )

    return "Tool loop limit reached; please try a simpler question."

if __name__ == "__main__":
    load_dotenv()

    # print("=" * 80)
    # print("LangChain + FAISS integration smoke test")
    # print("=" * 80)
    # print(f"Model: {os.getenv('OPENAI_MODEL', DEFAULT_MODEL)}")
    # print(f"Base URL: {os.getenv('OPENAI_BASE_URL', 'default OpenAI')}")
    # print(f"Handbook exists: {HANDBOOK_PATH.exists()}")
    # print("=" * 80)

    # api_key = os.getenv("OPENAI_API_KEY")
    # if not api_key:
    #     raise RuntimeError(
    #         "OPENAI_API_KEY is not set. Check your .env file."
    #     )

    # # 1. Handbook retrieval test
    query = "Tell me the actual MAC address."
    try:
        print("\n[1] Testing handbook retrieval...")
        handbook_query = query
        handbook_result = search_handbook.invoke({"query": handbook_query})
        print(f"Query: {handbook_query}")
        print("Result:")
        print(handbook_result[:1500] if handbook_result else "No result")
    except Exception as exc:
        print(f"[1] Handbook retrieval failed: {exc}")
        raise

    # # 2. Holiday tool test
    # try:
    #     print("\n" + "-" * 80)
    #     print("[2] Testing holiday tool...")
    #     holiday_date = "2026-12-25"
    #     holiday_result = check_holiday.invoke({"date": holiday_date})
    #     print(f"Date: {holiday_date}")
    #     print("Result:")
    #     print(holiday_result)
    # except Exception as exc:
    #     print(f"[2] Holiday tool failed: {exc}")
    #     raise

    # # 3. End-to-end chat test
    # try:
    #     print("\n" + "-" * 80)
    #     print("[3] Testing full chat pipeline...")
    #     user_question = (
    #         "Is 2026-12-25 a holiday?"
    #     )
    #     chat_result = run_chat(user_question)
    #     print(f"Question: {user_question}")
    #     print("Answer:")
    #     print(chat_result)
    # except Exception as exc:
    #     print(f"[3] Full chat pipeline failed: {exc}")
    #     raise

    # print("\n" + "=" * 80)
    # print("All integration checks passed.")
    # print("=" * 80)

    print(run_chat(query))
    # print(run_chat("How do I register my device?"))
    # print(run_chat("What are the rules for kitchen usage?"))
    # print(run_chat("What happens if I don’t label my food?"))