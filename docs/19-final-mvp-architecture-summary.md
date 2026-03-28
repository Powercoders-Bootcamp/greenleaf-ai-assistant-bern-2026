# Final MVP Architecture Summary

## 1. Product Position

Beat-Bot is a narrow internal policy assistant for GreenLeaf Logistics.

It is not a general-purpose chatbot, not a full HR system, and not a technical help desk.

The MVP is optimized for four core capabilities:

- source-backed handbook Q&A
- deterministic expense decisions
- deterministic Basel-Stadt holiday logic
- safe refusal and redirection behavior

## 2. Target Users and Access Model

The app is intended for internal project users.

### MVP Access Approach

- authentication via `Google Workspace OIDC`
- allowed domain: `@powercoders.org`
- simple role model:
  - `Employee`
  - `Admin`

This is a practical MVP access model for the project.

It is not a real GreenLeaf production identity environment.

## 3. Core Tech Stack

- `Frontend`: Next.js + TypeScript
- `Backend`: FastAPI
- `Database`: PostgreSQL + pgvector
- `LLM`: OpenAI API
- `Auth`: Google Workspace OIDC
- `Architecture style`: RAG + deterministic policy guardrails

## 4. Main Architectural Principle

The system follows this rule:

`Policy before generation`

That means:

- if a question can be answered deterministically, use rules
- if a question is sensitive, refuse or redirect
- only use retrieval + generation for supported handbook explanations

## 5. Main System Flow

1. User signs in with `@powercoders.org`
2. User submits a question in the web UI
3. Backend validates the request
4. Query classification runs
5. Policy layer decides the routing path
6. System either:
   - asks for clarification
   - returns a deterministic decision
   - refuses
   - redirects
   - or performs retrieval + generation
7. Response is validated
8. UI renders the result with citations when applicable

## 6. Query Classification Strategy

The MVP uses `hybrid classification`.

### First Pass

Deterministic signals:

- keywords
- phrase matching
- simple rules

### Second Pass

If the first pass is unclear:

- a lightweight classifier chooses from fixed labels

### Typical Classification Output

- `domain`
- `question_type`
- `sensitive`
- `needs_clarification`
- `routing_path`

## 7. Response Strategy

The MVP uses `hybrid response generation`.

### Template-Based Responses

Used for:

- clarification requests
- deterministic rule outcomes
- refusals
- redirects

### Retrieval Plus Generation

Used for:

- handbook explanations
- policy summaries
- source-backed informational answers

This keeps the risky parts controlled and the explanatory parts flexible.

## 8. Policy-First Domains

### Expense

Rule engine checks:

- amount above `35 CHF per person`
- alcohol included
- external client present
- enough info available

If required fields are missing, the app asks a template-based clarification question.

### Holidays

Deterministic logic checks:

- holiday date
- region
- Basel-Stadt handling
- May 1 rule

### Sensitive IT

The system refuses:

- internal Wi-Fi password requests
- guest Wi-Fi password requests in MVP
- MAC registration detail requests

The system may safely say:

- contact Sarah Muller in IT
- contact the IT desk

### Sensitive Conduct

The system redirects:

- harassment
- bullying
- whistleblowing

to the ombudsman process.

## 9. Retrieval Layer

RAG is still used, but only where appropriate.

The retrieval layer:

- indexes handbook content
- uses section-aware chunks
- stores metadata
- supports citation-friendly retrieval

Approved sources:

- Handbook v2.1
- Stakeholder Briefing
- Holiday CSV

## 10. Security Model

The key security rule is:

`Source presence does not equal disclosure permission`

So even if a sensitive detail appears in a source file, the bot does not automatically reveal it.

For MVP:

- no internal Wi-Fi credential disclosure
- no guest Wi-Fi password disclosure
- no MAC registration detail disclosure
- auth does not override these restrictions

## 11. MVP Scope Boundary

Included:

- handbook Q&A
- source citation
- expense decisions
- Basel holiday logic
- refusal and redirect flows
- lightweight internal auth

Deferred:

- advanced RBAC
- analytics/dashboard
- Slack/Teams integration
- OCR-based receipt processing
- production-grade enterprise identity setup

## 12. What Success Looks Like

The MVP is successful if an authenticated internal user can:

- ask a handbook question and get a cited answer
- ask an expense question and get a correct deterministic outcome
- ask a Basel holiday question and get the correct answer
- ask a sensitive IT question and get a safe refusal
- ask a misconduct question and get a redirect
