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
import logging
import sys
from datetime import datetime
from functools import lru_cache
from typing import Any
from zoneinfo import ZoneInfo
from pathlib import Path
import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from .holidays_checker import HolidayAPIError, is_day_a_holiday, parse_iso_date

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

HANDBOOK_CHUNK_SIZE = int(os.getenv("HANDBOOK_CHUNK_SIZE", "350"))
HANDBOOK_CHUNK_OVERLAP = int(os.getenv("HANDBOOK_CHUNK_OVERLAP", "50"))
HANDBOOK_RETRIEVAL_K = int(os.getenv("HANDBOOK_RETRIEVAL_K", "5"))

MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "6"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

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
    os.getenv("HANDBOOK_FAISS_DIR", "/app/runtime/vectorstore/handbook_faiss")
)

SESSION_TIMEZONE = ZoneInfo("Europe/Zurich")


def setup_logging() -> logging.Logger:
    log_level = LOG_LEVEL.upper()

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
        force=True,
    )

    return logging.getLogger(__name__)

logger = setup_logging()

logger.info(
    "\n=== CONFIGURATION ===\n"
    "OPENAI_API_KEY: %s\n"
    "OPENAI_BASE_URL: %s\n"
    "OPENAI_MODEL: %s\n"
    "OPENAI_EMBEDDING_MODEL: %s\n"
    "HANDBOOK_CHUNK_SIZE: %s\n"
    "HANDBOOK_CHUNK_OVERLAP: %s\n"
    "HANDBOOK_RETRIEVAL_K: %s\n"
    "MAX_TOOL_ROUNDS: %s\n"
    "LOG_LEVEL: %s\n"
    "REPO_ROOT: %s\n"
    "PROMPTS_DIR: %s\n"
    "SYSTEM_PROMPT_PATH exists: %s\n"
    "HANDBOOK_PATH exists: %s\n"
    "FAISS_DIR: %s\n"
    "FAISS index exists: %s\n"
    "SESSION_TIMEZONE: %s\n"
    "=====================",
    "***SET***" if OPENAI_API_KEY else "MISSING",
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENAI_EMBEDDING_MODEL,
    HANDBOOK_CHUNK_SIZE,
    HANDBOOK_CHUNK_OVERLAP,
    HANDBOOK_RETRIEVAL_K,
    MAX_TOOL_ROUNDS,
    LOG_LEVEL,
    REPO_ROOT,
    PROMPTS_DIR,
    SYSTEM_PROMPT_PATH.exists(),
    HANDBOOK_PATH.exists(),
    FAISS_DIR,
    (FAISS_DIR / "index.faiss").exists(),
    SESSION_TIMEZONE,
)

logger.info("FAISS_DIR writable: %s", os.access(FAISS_DIR, os.W_OK))


def load_system_prompt() -> str:
    logger.info("Loading system prompt from %s", SYSTEM_PROMPT_PATH)
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
    logger.info("Loading handbook from %s", HANDBOOK_PATH)
    if not HANDBOOK_PATH.is_file():
        raise FileNotFoundError(f"Handbook file not found: {HANDBOOK_PATH}")
    return HANDBOOK_PATH.read_text(encoding="utf-8")


def _split_handbook_into_documents(text: str) -> list[Document]:
    chunk_size = HANDBOOK_CHUNK_SIZE
    chunk_overlap = HANDBOOK_CHUNK_OVERLAP

    logger.info(
        "Splitting handbook into documents | chunk_size=%s | chunk_overlap=%s",
        chunk_size,
        chunk_overlap,
    )

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

    logger.info("Prepared %s handbook chunks", len(documents))
    return documents


def _build_vectorstore(embeddings: OpenAIEmbeddings) -> FAISS:
    logger.info("Building new FAISS vectorstore...")
    text = _load_handbook_text()
    documents = _split_handbook_into_documents(text)
    vectorstore = FAISS.from_documents(documents, embeddings)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(FAISS_DIR))
    logger.info("FAISS vectorstore saved to %s", FAISS_DIR)
    return vectorstore


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    llm_api_key = OPENAI_API_KEY
    if not llm_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    base_url = OPENAI_BASE_URL
    embedding_model = OPENAI_EMBEDDING_MODEL

    logger.info("Initializing embeddings model: %s", embedding_model)

    kwargs: dict[str, Any] = {
        "model": embedding_model,
        "api_key": llm_api_key,
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
        logger.info("Loading existing FAISS index from %s", FAISS_DIR)
        return FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    logger.info("FAISS index not found, creating a new one")
    return _build_vectorstore(embeddings)


@lru_cache(maxsize=1)
def get_retriever():
    k = HANDBOOK_RETRIEVAL_K
    return get_vectorstore().as_retriever(search_kwargs={"k": k})


def _format_docs_for_llm(docs: list[Document]) -> str:
    if not docs:
        logger.info("No relevant handbook sections were found.")
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
    logger.info("search_handbook called | query=%r", query)
    if not isinstance(query, str) or not query.strip():
        logger.warning("search_handbook received invalid query")
        return "Invalid query: provide a non-empty string."

    docs = get_retriever().invoke(query)
    logger.info("search_handbook returned %s documents", len(docs))
    return _format_docs_for_llm(docs)


@tool
def check_holiday(date: str) -> str:
    """
    Check whether the given ISO date (YYYY-MM-DD) is a holiday.
    """
    logger.info("check_holiday called | query=%r", date)

    day = parse_iso_date(date) if isinstance(date, str) else None
    if day is None:
        logger.warning("Invalid date passed to check_holiday: %r", date)
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
    except HolidayAPIError as excep:
        logger.exception("Holiday API failed")
        return json.dumps({"error": str(excep)}, ensure_ascii=False)


def get_llm() -> ChatOpenAI:
    llm_api_key = OPENAI_API_KEY
    if not llm_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    model = OPENAI_MODEL
    base_url = OPENAI_BASE_URL

    kwargs: dict[str, Any] = {
        "model": model,
        "api_key": llm_api_key,
        "temperature": 0,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)


def _convert_history(conversation_messages: list[dict[str, str]]) -> list[Any]:
    logger.info("Adding conversation history...")
    result = []

    for msg in conversation_messages:
        role = msg.get("role")
        content = msg.get("content", "")

        if role == "user":
            result.append(HumanMessage(content=content))
        elif role == "assistant":
            result.append(AIMessage(content=content))

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
        logger.info("Loading conversation history | messages=%s", len(conversation_messages))
        messages.extend(_convert_history(conversation_messages))

    messages.append(HumanMessage(content=user_message))

    for round_num in range(1, MAX_TOOL_ROUNDS + 1):
        logger.info("LLM round %s/%s", round_num, MAX_TOOL_ROUNDS)

        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        tool_calls = getattr(ai_msg, "tool_calls", None) or []
        logger.info("Tool calls in this round: %s", len(tool_calls))

        if not tool_calls:
            text = _stringify_content(ai_msg.content)
            logger.info("Final assistant response produced")
            return text or "The model returned an empty response."

        for call in tool_calls:
            tool_name = call["name"]
            tool_args = call.get("args", {})
            tool_call_id = call["id"]

            logger.info("Executing tool | name=%s | args=%s", tool_name, tool_args)

            selected_tool = tool_registry.get(tool_name)
            if selected_tool is None:
                logger.error("Unknown tool requested: %s", tool_name)
                tool_result = json.dumps(
                    {"error": f"Unknown tool: {tool_name}"},
                    ensure_ascii=False,
                )
            else:
                try:
                    # LangChain tools accept dict input for structured args
                    tool_result = selected_tool.invoke(tool_args)
                    logger.info("Tool %s executed successfully", tool_name)
                except Exception as exep:  # defensive: keep the loop alive
                    logger.exception("Tool execution failed | tool=%s", tool_name)
                    tool_result = json.dumps(
                        {"error": f"Tool execution failed: {exep}"},
                        ensure_ascii=False,
                    )

            messages.append(
                ToolMessage(
                    content=_stringify_content(tool_result),
                    tool_call_id=tool_call_id,
                )
            )

    logger.warning("Tool loop limit reached")
    return "Tool loop limit reached; please try a simpler question."
