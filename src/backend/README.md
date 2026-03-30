# Backend

This folder will contain the assistant logic, including:
- handbook and holiday data loading
- retrieval and citation handling
- structured LLM draft generation
- post-generation validation
- safe fallback handling
- auth, chat history, and admin review support

Planned responsibilities:
- validate expenses
- validate holiday logic
- prevent unsafe answers
- return structured responses with sources
- persist chat history and related metadata

Recommended implementation references:

- `docs/22-backend-component-map.md`
- `docs/24-structured-llm-response-schema.md`
- `docs/25-backend-implementation-blueprint.md`
