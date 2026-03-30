# Target Architecture

## GreenLeaf Logistics - Beat-Bot

## 1. Architecture Summary

Beat-Bot uses an LLM-first RAG architecture with lightweight post-generation guardrails.

The system is designed as a `modular monolith`, not a microservice system.

The main idea is simple:

- let the LLM interpret the user question and draft the response
- ground supported answers in approved sources
- validate the draft before anything reaches the user
- fall back safely when the draft fails a critical check

## 2. Core Stack

- `Frontend`: Next.js + Javascript
- `Backend`: FastAPI
- `Database`: PostgreSQL + pgvector
- `LLM / helper AI`: OpenAI API
- `Auth`: required for MVP

## 3. Core Architectural Principle

`Generate first, validate before release`

This means:

- the LLM is responsible for interpreting the question and drafting the answer
- the backend still performs structured safety and consistency checks
- no response should reach the user unless it passes validation or a safe fallback is applied

## 4. Main Runtime Flow

1. user authenticates through the chosen internal-access method
2. user submits a question in the web UI
3. backend validates the request
4. input is normalized into the common text-query format
5. the LLM produces a structured draft response
6. validators check the draft for safety, citations, and consistency
7. the system either:
   - returns the validated draft
   - retries with a stricter instruction
   - or returns a safe fallback
8. audit events are recorded

## 5. Main Components

- `API layer`: receives requests and returns structured responses
- `Auth module`: validates identity, manages sessions, and resolves role mapping from the app database
- `Input processing`: normalizes text and supports future translation/transcription adapters
- `Retrieval`: evidence lookup from approved sources
- `Answer generation`: creates a structured draft response from the user question and approved evidence
- `Response validator`: enforces schema, citation, disclosure, and consistency checks
- `Fallback handler`: retries or returns a safe refusal/redirect/verification failure response
- `Audit/logging`: traceability and debugging support
- `Chat history storage`: persistent conversation history and metadata with role-based visibility

The developer-facing backend breakdown is documented in `22-backend-component-map.md`.

## 6. Structured LLM Drafts

The LLM should return a structured draft, not only free text.

Recommended fields include:

- `answer_text`
- `response_type`
- `citations`
- `decision`
- `needs_clarification`
- `sensitive_topic`

This gives the backend a stable object to validate instead of relying on brittle string matching alone.

## 7. AI Usage

The OpenAI API is used as the main interpretation and answer-drafting layer.

It may also support:

- translation or normalization
- future speech-to-text transcription

Important boundary:

- the LLM drafts the answer
- the backend decides whether that draft is safe and acceptable to release

## 8. Post-Generation Validators

Lightweight validators should run after draft generation.

Best-practice implementation rule:

- trust structured output more than prose
- trust backend validation more than model self-report
- prefer safe fallback over uncertain release

Recommended validators:

- `schema validator`
  - ensures the draft contains the expected fields
- `citation validator`
  - trusted policy-style answers should include citations
- `disclosure validator`
  - blocks credential leakage and restricted technical disclosure
- `consistency validator`
  - checks high-risk business rules against narrow structured facts
- `response-type validator`
  - ensures harassment-like questions become redirects and Wi-Fi/password questions become refusals

Validators should prefer structured facts over raw substring matching.

For example:

- do not hardcode only `36 CHF`; extract amount and compare numerically against the `35 CHF per person` rule
- do not ban the phrase `MAC address` everywhere; allow safe refusal text while blocking actionable disclosure

## 9. Validation Outcomes

If validation fails, the system should:

- retry once with a stricter instruction when useful
- otherwise return a safe fallback
- never release a draft that fails a critical disclosure or misconduct check

## 10. High-Risk Domains

The validator layer must be especially careful for:

- expense decisions
- Basel holiday handling
- Wi-Fi and MAC topics
- harassment, bullying, and whistleblowing

For these areas, the system should combine:

- grounded source retrieval where relevant
- structured LLM output
- narrow backend validation rules
- safe fallback behavior

## 11. Data and Retrieval

Approved source set:

- Handbook v2.1
- Stakeholder Briefing
- 2026 Holiday CSV

Retrieval should:

- use section-aware chunks
- preserve metadata
- support citation-ready evidence
- filter by domain and sensitivity when needed

## 12. Security Boundary

`Source presence does not equal disclosure permission`

Even if a source document contains a sensitive detail, the bot may still need to refuse disclosure.

This is especially important for:

- Wi-Fi credentials
- technical access information
- device-registration details

## 12.1 LLM Data-Access Boundary

Best-practice boundary:

- the LLM must not connect directly to the database
- the LLM must not own identity, role, or authorization logic
- the backend should pass only the minimum necessary context for a single request

In practice, this means:

- user data stays in backend-controlled storage
- role mapping stays in backend-controlled storage
- full chat history is not exposed to the LLM by default
- only selected, relevant, and sanitized context may be included in a prompt when needed

## 13. Future Extensibility

The system should remain:

- `text-first`
- `input-channel agnostic`

This allows future additions such as:

- voice input adapter
- translation/normalization helper path
- OCR or receipt-processing path

without rewriting the core policy pipeline.

## 14. Auth and Access Decisions Already Locked

The following product decisions are now fixed for MVP:

- user login is required
- the role model is `Employee` and `Admin`
- app access is identity-based only for now
- role mapping should live in the application database
- `Admin` can review all employee chat histories and related metadata
- each `Employee` can review only their own chat history

The remaining auth clarification is limited to the concrete provider or mechanism, not whether login exists.
