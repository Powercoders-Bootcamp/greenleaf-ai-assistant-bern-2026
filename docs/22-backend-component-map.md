# Backend Component Map

## 1. Main Structure

A modular backend is recommended inside a single service:

- `api`
- `auth`
- `input_processing`
- `retrieval`
- `generation`
- `validation`
- `fallbacks`
- `responses`
- `audit`
- `shared`

This is not a microservice architecture.

It is a `modular monolith` with clear internal boundaries.

## 2. Component Responsibilities

### `api`

HTTP layer.

Responsibilities:

- accept requests
- return responses
- validate schemas
- define routes
- handle errors

Example endpoints:

- `POST /ask`
- `GET /health`

### `auth`

Authentication and basic role resolution.

Responsibilities:

- validate the chosen login/session mechanism
- read user email
- resolve role mapping from the application database
- expose `Employee` or `Admin`

### `input_processing`

Normalizes inputs into a shared internal format.

Responsibilities:

- text input normalization
- future translation helper
- future transcription helper
- language detection
- unified query object creation

This keeps the core pipeline compatible with future input channels such as voice.

### `retrieval`

Evidence lookup layer.

Responsibilities:

- query embedding
- vector search
- metadata filtering
- select top chunks
- return citation candidates

### `generation`

Primary LLM interaction layer.

Responsibilities:

- grounded draft generation
- structured output generation
- clarification-aware response drafting
- handbook explanation responses

This module drafts the answer, but does not decide whether it is safe to release.

### `validation`

Post-generation guardrail layer.

Responsibilities:

- schema validation
- citation validation
- disclosure validation
- expense and holiday consistency checks
- response-type checks for refusal and redirect scenarios

Validators should work from structured fields whenever possible, not from brittle raw-string checks alone.

### `fallbacks`

Safe recovery layer.

Responsibilities:

- retry draft generation with stricter instructions
- return a safe refusal when disclosure validation fails
- return a safe redirect when misconduct handling is required
- return a verification failure message when a trustworthy answer cannot be confirmed

### `responses`

Builds user-facing responses.

Responsibilities:

- final response formatting
- citation rendering
- safe fallback formatting

This module only formats outputs that have already passed validation or been replaced by a safe fallback.

### `audit`

Traceability and logging layer.

Responsibilities:

- log request metadata
- log structured draft metadata
- log validator outcomes
- log retrieval trace
- log response type
- log fallback reason when used
- persist chat history and access-control metadata

### `shared`

Shared internal models and utilities.

Responsibilities:

- data models
- enums
- constants
- config
- common helpers

## 3. Recommended Request Flow Across Components

Recommended flow:

`api -> auth -> input_processing -> retrieval -> generation -> validation -> fallbacks -> responses -> audit`

Not every request uses every module.

### Example: Expense Question

`api -> auth -> input_processing -> retrieval -> generation -> validation -> fallbacks -> responses -> audit`

### Example: Handbook Explanation Question

`api -> auth -> input_processing -> retrieval -> generation -> validation -> responses -> audit`

### Example: Sensitive IT Question

`api -> auth -> input_processing -> retrieval -> generation -> validation -> fallbacks -> responses -> audit`

## 4. Example Folder Shape

```text
src/backend/
  api/
    routes/
    schemas/
  auth/
    oidc.py
    roles.py
  input_processing/
    normalizer.py
    language.py
    translation.py
    transcription.py
  retrieval/
    store.py
    search.py
    filters.py
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
    models.py
    enums.py
    config.py
  main.py
```

## 5. Design Rules

- `generation` drafts, but does not release
- `validation` decides whether a draft is acceptable
- `fallbacks` recover safely when validation fails
- `responses` formats user-facing output
- `audit` records important pipeline events
- `input_processing` keeps future voice and multilingual support isolated from the core answer pipeline

## 6. Most Critical Boundaries

The most important architectural boundaries are:

- `generation` and `validation` must not be mixed
- `auth` and security-disclosure policy must not be confused
- `input_processing` must stay separate from the core answer pipeline
- `retrieval` finds evidence, but does not decide outcomes

## 7. MVP-Minimum Version

If the team wants the smallest practical backend for MVP, the minimum version can start with:

- `api`
- `auth`
- `retrieval`
- `generation`
- `validation`
- `fallbacks`
- `responses`
- `shared`

`input_processing` and `audit` can start thin and expand later.
