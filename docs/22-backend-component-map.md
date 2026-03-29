# Backend Component Map

## 1. Main Structure

A modular backend is recommended inside a single service:

- `api`
- `auth`
- `input_processing`
- `classification`
- `policy`
- `retrieval`
- `generation`
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

- validate OIDC token or session
- read user email
- resolve role mapping
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

### `classification`

Assigns routing labels to the question.

Responsibilities:

- deterministic keyword and pattern pass
- fallback classifier
- structured classification output

Typical output:

- `domain`
- `question_type`
- `sensitive`
- `needs_clarification`
- `routing_path`

### `policy`

The most critical business-decision module.

Responsibilities:

- expense rules
- holiday rules
- sensitive IT refusal
- misconduct redirect
- clarification requirement detection

Possible submodules:

- `expense_policy`
- `holiday_policy`
- `security_policy`
- `conduct_policy`

### `retrieval`

Evidence lookup layer.

Responsibilities:

- query embedding
- vector search
- metadata filtering
- select top chunks
- return citation candidates

### `generation`

Used only when natural-language explanation is needed.

Responsibilities:

- grounded answer generation
- structured output generation
- handbook explanation responses

This module should not make final policy decisions.

### `responses`

Builds user-facing responses.

Responsibilities:

- clarification template rendering
- refusal template rendering
- redirect template rendering
- deterministic decision formatting
- generated answer formatting

This module ensures rule-based and safety-critical responses do not depend on free-form generation.

### `audit`

Traceability and logging layer.

Responsibilities:

- log request metadata
- log classification result
- log applied rules
- log retrieval trace
- log response type
- log refusal or redirect reason

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

`api -> auth -> input_processing -> classification -> policy -> retrieval -> generation -> responses -> audit`

Not every request uses every module.

### Example: Expense Question

`api -> auth -> input_processing -> classification -> policy -> responses -> audit`

### Example: Handbook Explanation Question

`api -> auth -> input_processing -> classification -> policy -> retrieval -> generation -> responses -> audit`

### Example: Sensitive IT Question

`api -> auth -> input_processing -> classification -> policy -> responses -> audit`

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
  classification/
    rules.py
    classifier.py
    schema.py
  policy/
    expense.py
    holidays.py
    security.py
    conduct.py
    router.py
  retrieval/
    store.py
    search.py
    filters.py
  generation/
    prompts.py
    answer_generator.py
    structured_output.py
  responses/
    templates.py
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

- `classification` routes, but does not make business decisions
- `policy` makes business decisions
- `generation` explains, but does not override policy
- `responses` formats user-facing output
- `audit` records important pipeline events
- `input_processing` keeps future voice and multilingual support isolated from core policy logic

## 6. Most Critical Boundaries

The most important architectural boundaries are:

- `policy` and `generation` must not be mixed
- `auth` and security-disclosure policy must not be confused
- `input_processing` must stay separate from core policy logic
- `retrieval` finds evidence, but does not decide outcomes

## 7. MVP-Minimum Version

If the team wants the smallest practical backend for MVP, the minimum version can start with:

- `api`
- `auth`
- `classification`
- `policy`
- `retrieval`
- `generation`
- `responses`
- `shared`

`input_processing` and `audit` can start thin and expand later.
