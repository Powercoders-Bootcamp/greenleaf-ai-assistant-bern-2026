# Target Architecture

## GreenLeaf Logistics - Beat-Bot

## 1. Architecture Summary

Beat-Bot uses a policy-first RAG architecture.

The system is designed as a `modular monolith`, not a microservice system.

The main idea is simple:

- use deterministic policy logic whenever the business rule is explicit
- use retrieval plus generation only for supported handbook explanations
- refuse or redirect when the topic is sensitive

## 2. Core Stack

- `Frontend`: Next.js + TypeScript
- `Backend`: FastAPI
- `Database`: PostgreSQL + pgvector
- `LLM / helper AI`: OpenAI API
- `Auth`: clarification required, with Google Workspace OIDC as the current working assumption

## 3. Core Architectural Principle

`Policy before generation`

This means:

- expense, holiday, and security-sensitive questions should not be decided by free-form generation
- the model may help with understanding or transformation tasks
- business decisions remain inside the policy layer

## 4. Main Runtime Flow

1. user authenticates through the chosen internal-access method
2. user submits a question in the web UI
3. backend validates the request
4. input is normalized into the common text-query format
5. query classification runs
6. policy router chooses the path
7. system returns one of:
   - clarification
   - deterministic decision
   - refusal
   - redirect
   - retrieval plus generated explanation
8. response is validated
9. audit events are recorded

## 5. Main Components

- `API layer`: receives requests and returns structured responses
- `Auth module`: validates identity and resolves role mapping
- `Input processing`: normalizes text and supports future translation/transcription adapters
- `Classification`: hybrid routing layer
- `Policy engine`: deterministic rules and safety decisions
- `Retrieval`: evidence lookup from approved sources
- `Answer generation`: evidence-based explanatory answers only
- `Response templates`: clarification, refusal, redirect, and deterministic responses
- `Response validator`: schema and safety checks
- `Audit/logging`: traceability and debugging support

The developer-facing backend breakdown is documented in `22-backend-component-map.md`.

## 6. Hybrid Classification

Beat-Bot should use:

### First pass

- deterministic keywords
- pattern matching
- simple routing rules

### Second pass

If the first pass is uncertain, the system may use a constrained AI helper step that returns a fixed schema such as:

- `domain`
- `question_type`
- `sensitive`
- `needs_clarification`
- `routing_path`

## 7. Hybrid Response Strategy

The app should not use one response method for every case.

### Template-based responses

Use templates for:

- clarification requests
- deterministic rule outcomes
- refusals
- redirects

### Retrieval plus generation

Use retrieval plus generation for:

- handbook explanations
- policy summaries
- source-backed informational responses

## 8. AI-Assisted Helper Services

The OpenAI API may be used for tightly scoped helper tasks:

- classification fallback
- translation or normalization
- future speech-to-text transcription

Important boundary:

- AI may help with understanding and transformation
- AI should not make final policy decisions for expense, holiday, security, or misconduct-routing cases

## 9. Policy-First Domains

### Expense

Deterministic checks:

- amount above `35 CHF per person`
- alcohol included
- external client present
- enough decision data available

### Holidays

Deterministic checks:

- holiday date
- region
- Basel-Stadt handling
- May 1 rule

### Sensitive IT

The app refuses:

- internal Wi-Fi password requests
- guest Wi-Fi password requests in the MVP
- MAC registration detail requests

The app may provide safe process guidance such as contacting IT.

### Sensitive Conduct

The app redirects:

- harassment
- bullying
- whistleblowing

to the ombudsman process.

## 10. Data and Retrieval

Approved source set:

- Handbook v2.1
- Stakeholder Briefing
- 2026 Holiday CSV

Retrieval should:

- use section-aware chunks
- preserve metadata
- support citation-ready evidence
- filter by domain and sensitivity when needed

## 11. Security Boundary

`Source presence does not equal disclosure permission`

Even if a source document contains a sensitive detail, the bot may still need to refuse disclosure.

This is especially important for:

- Wi-Fi credentials
- technical access information
- device-registration details

## 12. Future Extensibility

The system should remain:

- `text-first`
- `input-channel agnostic`

This allows future additions such as:

- voice input adapter
- translation/normalization helper path
- OCR or receipt-processing path

without rewriting the core policy pipeline.
