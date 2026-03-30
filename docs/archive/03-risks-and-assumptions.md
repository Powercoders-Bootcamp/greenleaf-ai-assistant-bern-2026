# Risks and Assumptions

> Archive note: This document is kept for historical context. The current architecture is `LLM-first + structured validators + safe fallback`.

## GreenLeaf Logistics - Beat-Bot

## 1. Core Assumptions

- the handbook and stakeholder briefing are the source of truth for MVP behavior
- a narrow MVP is more valuable than a broad but unreliable assistant
- retrieval quality can be acceptable if chunking and metadata are handled carefully
- login, role mapping, and chat history will be handled in backend-controlled storage

## 2. Critical Risks

### R1 - Retrieval quality risk

Weak retrieval can lead to incorrect answers or weak citations.

### R2 - Hallucination risk

If the model answers beyond evidence, trust will collapse quickly.

### R3 - Holiday logic risk

If Basel-Stadt handling is wrong, the product fails a core sponsor requirement.

### R4 - Expense policy risk

If the 35 CHF and alcohol rules are not enforced correctly, the product fails a core sponsor requirement.

### R5 - Security interpretation risk

If Wi-Fi or MAC-related topics are handled loosely, the bot may leak information the sponsor considers unsafe.

### R6 - Scope creep risk

If the team tries to cover every handbook topic equally, the MVP may become late and unreliable.

## 3. Risk Mitigations

- use structured post-generation validators for expense, holiday, disclosure, and response type
- require source-backed answers
- refuse when confidence or grounding is weak
- treat Wi-Fi and MAC questions conservatively in the MVP
- prioritize a small golden question set early
- cut optional features before cutting safety controls
