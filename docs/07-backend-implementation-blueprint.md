# Backend Implementation Blueprint

## GreenLeaf Logistics - Beat-Bot

## 1. Goal

This document turns the backend architecture into a practical implementation plan.

It defines:

- the recommended backend tech stack
- the project folder structure
- the main modules and responsibilities
- the minimum MVP setup

## 2. Recommended Backend Tech Stack

### Core Application

- `Python 3.12`
- `FastAPI`
- `Uvicorn`
- `Pydantic v2`

### Database

- `PostgreSQL`
- `pgvector`
- `SQLAlchemy 2.x`
- `Alembic`

### LLM and Embeddings

- `OpenAI API`
- OpenAI chat/completions for structured draft generation
- OpenAI embeddings for retrieval indexing and search

### Authentication

- session-based or token-based login mechanism
- final provider/mechanism still to be chosen
- app-side role mapping stored in the database

### Validation and Safety

- Pydantic schemas for structured LLM output
- custom validator modules for:
  - citations
  - disclosure
  - consistency
  - response type

### Data Processing

- `pypdf` or equivalent PDF text extraction library
- `csv` or `pandas` for holiday CSV ingestion

### Testing

- `pytest`
- `pytest-asyncio`
- `httpx`

### Developer Tooling

- `ruff`
- `black`
- `mypy`

## 3. Why This Stack Fits the Project

This stack is a good fit because:

- `FastAPI` is fast for MVP delivery and works well with typed request/response models
- `Pydantic` is ideal for structured LLM draft parsing
- `PostgreSQL + pgvector` supports both app data and retrieval data in one place
- `SQLAlchemy + Alembic` gives enough structure without adding heavy complexity
- Python is strong for data ingestion, validation, and AI integration

## 4. Recommended Backend Folder Structure

```text
src/backend/
  app/
    api/
      routes/
        ask.py
        auth.py
        admin.py
        history.py
        health.py
      schemas/
        ask.py
        auth.py
        history.py
    auth/
      service.py
      roles.py
      dependencies.py
    db/
      base.py
      session.py
      models/
        user.py
        chat.py
        message.py
        source_chunk.py
      migrations/
    input_processing/
      normalizer.py
      language.py
    ingestion/
      handbook_loader.py
      holiday_loader.py
      chunking.py
      embeddings.py
    retrieval/
      search.py
      filters.py
      citations.py
    generation/
      prompts.py
      answer_generator.py
      structured_output.py
    validation/
      schema.py
      citations.py
      disclosure.py
      consistency.py
      response_type.py
    fallbacks/
      retry.py
      safe_responses.py
    responses/
      formatter.py
    audit/
      logger.py
      events.py
    shared/
      config.py
      enums.py
      constants.py
      exceptions.py
      utils.py
    main.py
  tests/
    unit/
    integration/
    e2e/
  README.md
```

## 5. Main Module Responsibilities

### `api`

Responsibilities:

- receive HTTP requests
- validate input payloads
- call the application flow
- return final responses

Recommended MVP endpoints:

- `POST /ask`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /me`
- `GET /history`
- `GET /admin/chats`
- `GET /health`

### `auth`

Responsibilities:

- verify the chosen login/session mechanism
- load the current user
- resolve `Employee` or `Admin`
- enforce access checks for history and admin routes

### `db`

Responsibilities:

- database session management
- ORM models
- migrations
- persistence for users, roles, chats, messages, and retrieval data

### `ingestion`

Responsibilities:

- extract text from the handbook
- chunk handbook content
- load holiday CSV data
- create and store embeddings

### `retrieval`

Responsibilities:

- embed or transform the user query
- search relevant chunks
- return grounded evidence
- prepare citation metadata

### `generation`

Responsibilities:

- build prompts
- call the LLM
- parse structured draft output

This module drafts the answer but does not release it directly.

### `validation`

Responsibilities:

- validate the structured schema
- require citations where needed
- block restricted disclosure
- check high-risk consistency for:
  - expenses
  - holidays
  - misconduct redirects
  - Wi-Fi/MAC restrictions

### `fallbacks`

Responsibilities:

- retry a failed generation once when recoverable
- return safe fallback responses

### `responses`

Responsibilities:

- transform validated drafts into final API responses
- format citations
- return user-safe response payloads

### `audit`

Responsibilities:

- log validator outcomes
- log fallback reasons
- store conversation metadata
- support admin review visibility

## 6. Recommended Database Tables

Minimum MVP tables:

- `users`
- `chats`
- `messages`
- `source_chunks`
- `source_documents`

Recommended key fields:

### `users`

- `id`
- `email`
- `role`
- `is_active`
- `created_at`

### `chats`

- `id`
- `user_id`
- `title`
- `created_at`

### `messages`

- `id`
- `chat_id`
- `sender_type`
- `message_text`
- `response_type`
- `validator_status`
- `created_at`

### `source_documents`

- `id`
- `name`
- `version`
- `source_type`

### `source_chunks`

- `id`
- `document_id`
- `section`
- `page`
- `content`
- `embedding`

## 7. Recommended MVP Runtime Flow

```text
POST /ask
  -> auth check
  -> input normalization
  -> retrieval
  -> LLM structured draft generation
  -> schema validation
  -> citation/disclosure/consistency/response-type validation
  -> retry or safe fallback if needed
  -> final response formatting
  -> audit logging
  -> message persistence
```

## 8. Recommended Environment Variables

```text
APP_ENV=
APP_SECRET_KEY=
DATABASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=
OPENAI_EMBEDDING_MODEL=
SESSION_COOKIE_NAME=
SESSION_COOKIE_SECURE=
LOG_LEVEL=
```

If auth later uses an external provider, add:

```text
AUTH_PROVIDER=
AUTH_CLIENT_ID=
AUTH_CLIENT_SECRET=
AUTH_REDIRECT_URI=
```

## 9. MVP-Minimum Package Set

If the team wants the smallest practical backend, start with:

- `app/api`
- `app/auth`
- `app/db`
- `app/ingestion`
- `app/retrieval`
- `app/generation`
- `app/validation`
- `app/fallbacks`
- `app/responses`
- `app/shared`

Add `audit` and richer admin/reporting features immediately after the main ask-flow works.

## 10. Recommended Build Order

1. FastAPI app bootstrap
2. DB session and base models
3. user login and role loading
4. handbook and holiday ingestion
5. retrieval layer
6. structured LLM generation
7. validator pipeline
8. safe fallback handling
9. chat history persistence
10. admin history view
11. tests and golden-set verification

## 11. Best-Practice Notes

- keep the backend as a modular monolith for MVP
- use structured LLM output everywhere possible
- do not mix generation and validation logic
- keep validators small, explicit, and testable
- persist enough metadata for admin review, but avoid storing unnecessary secrets
- optimize for correctness and safe failure, not cleverness
- keep identity, role mapping, and access control in backend code and database layers
- pass only minimum necessary context to the LLM for each request
