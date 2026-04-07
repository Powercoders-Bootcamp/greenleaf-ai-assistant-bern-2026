from __future__ import annotations

import re


def extract_amounts(text: str) -> list[str]:
    return re.findall(r"\b\d+\s*CHF\b", text, flags=re.IGNORECASE)


def build_keywords(message: str, classification: str) -> list[str]:
    keywords = [message.strip()]
    lower_message = message.lower()

    if classification == "expense_policy":
        keywords.extend([
            "expense",
            "client lunch",
            "reimbursable",
            "35 CHF",
            "alcohol",
            "wine",
            "receipt",
            "external client",
        ])

    elif classification == "leave_policy":
        keywords.extend([
            "vacation",
            "annual leave",
            "holiday",
            "May 1st",
            "Basel-Stadt",
        ])

    elif classification == "it_security":
        keywords.extend([
            "password",
            "Wi-Fi",
            "MAC address",
            "laptop",
            "IT desk",
        ])

    elif classification == "conduct":
        keywords.extend([
            "harassment",
            "bullying",
            "whistleblowing",
            "ombudsman",
            "confidential",
        ])

    keywords.extend(extract_amounts(message))

    deduped: list[str] = []
    seen: set[str] = set()

    for keyword in keywords:
        normalized = keyword.strip()
        if normalized and normalized.lower() not in seen:
            deduped.append(normalized)
            seen.add(normalized.lower())

    return deduped