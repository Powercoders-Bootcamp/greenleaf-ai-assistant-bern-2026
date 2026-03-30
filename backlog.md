# Product Backlog

## Project

**Project Name:** GreenLeaf Logistics Beat-Bot  
**Primary Sponsor:** Beat Muller, Head of Operations & HR  
**Goal:** Deliver a trusted internal AI assistant that answers repetitive employee policy questions from approved company sources, enforces hard business rules, and refuses unsafe or out-of-scope requests.

## Source-Informed Product Scope

The backlog below is aligned to the current known sources:

- `GreenLeaf Logistics Internal Handbook v2.1`
- `Stakeholder Briefing: The "Beat-Bot" Project`
- `2026 Holiday Logic (CSV)`

These sources make four capabilities non-negotiable:

- source-backed handbook Q&A
- deterministic expense decisions
- Basel-Stadt holiday accuracy
- security-first refusal and redirection behavior

## Backlog Principles

- Accuracy over creativity
- Source-backed answers only
- Validate before release
- Security by default
- Refuse when evidence is weak
- Keep MVP narrow and reliable

## Important Product Interpretation

The handbook contains the current guest Wi-Fi password. The stakeholder briefing explicitly says the bot must not give out internal Wi-Fi passwords or MAC address details "to just anyone." For the MVP, the safest interpretation is:

- never disclose internal Wi-Fi credentials
- never disclose MAC address registration details beyond directing users to IT
- do not disclose the guest Wi-Fi password through the bot
- redirect Wi-Fi access requests to IT or the appropriate human-managed process

This can be revisited later with explicit role-based approval.

For MVP authentication, user login is required. The MVP must support authenticated access with two application roles:

- `Employee`
- `Admin`

Google Workspace OIDC is not the chosen provider for now. The authentication mechanism still needs implementation design, but authenticated access itself is no longer optional.

The earlier plan to use keyword-based pre-classification and template-first response routing is no longer in scope. The current direction is an `LLM-first` flow with structured post-generation validators and safe fallbacks.

## Priority Scale

- `Must Have` - Required for MVP success
- `Should Have` - Important, but not required for first release
- `Could Have` - Valuable enhancement if time allows
- `Won't Have` - Explicitly out of scope for this phase

## Estimation Scale

- `S` - Small
- `M` - Medium
- `L` - Large

## Epic 1: Product Foundation and Delivery Setup

### BB-001 - Project repository and working agreements

**Priority:** Must Have  
**Estimate:** S  
**Story:** As a project team, we want a clear repo structure and delivery conventions so that we can work consistently.

**Acceptance Criteria**
- Repository structure is agreed and documented
- Branching and PR conventions are defined
- Roles and ownership are visible
- Definition of Ready and Definition of Done are linked from the repo

### BB-002 - Environment setup for frontend, backend, and data work

**Priority:** Must Have  
**Estimate:** M  
**Story:** As a developer, I want a working local setup so that I can contribute without setup blockers.

**Acceptance Criteria**
- Frontend can run locally
- Backend can run locally
- Required environment variables are documented
- Local development instructions are written

### BB-003 - Shared API and data contracts

**Priority:** Must Have  
**Estimate:** M  
**Story:** As a team, we want shared request and response contracts so that frontend and backend integrate smoothly.

**Acceptance Criteria**
- Request schema for asking a question is defined
- Response schema includes answer, sources, confidence, refusal flag, and policy metadata
- Error response format is documented
- Contract examples are available

## Epic 2: User Interface

### BB-004 - Basic internal chat interface

**Priority:** Must Have  
**Estimate:** M  
**Story:** As an employee, I want a simple interface so that I can ask policy questions easily.

**Acceptance Criteria**
- User can type a question and submit it
- Conversation area shows user and assistant messages
- Interface works on desktop and mobile screen sizes
- UI remains usable with long answers

### BB-005 - Loading, error, and empty states

**Priority:** Must Have  
**Estimate:** S  
**Story:** As an employee, I want clear feedback while the system works so that the experience feels reliable.

**Acceptance Criteria**
- Loading state appears while waiting for backend response
- Network or server errors are shown clearly
- Empty or invalid input is handled gracefully

### BB-006 - Source citation display

**Priority:** Must Have  
**Estimate:** S  
**Story:** As an employee, I want to see the source of each answer so that I can verify the result.

**Acceptance Criteria**
- Each answer can display one or more citations
- Citation label is human-readable
- Source metadata includes at least section or document name

### BB-007 - Refusal and redirection UI states

**Priority:** Must Have  
**Estimate:** S  
**Story:** As an employee, I want refusals and redirects to be clearly explained so that I know what to do next.

**Acceptance Criteria**
- Refusal responses are visually distinguishable from normal answers
- Redirect responses can show the proper channel or next step
- Sensitive-topic responses do not expose restricted content

### BB-008 - Response formatting for structured outputs

**Priority:** Must Have  
**Estimate:** S  
**Story:** As an employee, I want answers to be clearly formatted so that I can understand them quickly.

**Acceptance Criteria**
- Answer body is separated from sources
- Confidence or policy status can be displayed when available
- Long answers remain readable

## Epic 3: Backend API and Orchestration

### BB-009 - Health check and base API structure

**Priority:** Must Have  
**Estimate:** S  
**Story:** As a developer, I want a working API skeleton so that other features can be integrated safely.

**Acceptance Criteria**
- Backend service starts successfully
- Health endpoint is available
- Base routing structure exists

### BB-010 - `/ask` endpoint

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the frontend, I want a stable `/ask` endpoint so that the user can submit questions.

**Acceptance Criteria**
- Endpoint accepts a validated question payload
- Endpoint returns a structured response
- Invalid input returns a safe error response

### BB-011 - Request orchestration pipeline

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want one orchestration flow for every request so that retrieval, draft generation, validation, and fallback happen consistently.

**Acceptance Criteria**
- Retrieval and generation steps are centrally coordinated
- The LLM returns a structured draft response
- Post-generation validators run before any response is released
- Retry and safe fallback behavior are centrally coordinated
- Response validation runs before output is returned

### BB-012 - Structured response validation

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want to validate generated responses so that broken or unsafe outputs are not returned.

**Acceptance Criteria**
- Output schema is enforced server-side
- Missing citations trigger fallback or refusal
- Invalid fields are rejected before response is sent

## Epic 4: Source Management, Ingestion, and Knowledge Base

### BB-013 - Source inventory and approval list

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the team, we want a defined list of approved sources so that the assistant only answers from trusted content.

**Acceptance Criteria**
- Approved source list is documented
- Each source has a version or date reference
- Out-of-scope sources are excluded from ingestion

### BB-014 - Handbook parsing pipeline

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want to parse the handbook so that it can be searched.

**Acceptance Criteria**
- Handbook PDF can be parsed
- Parsed content preserves section boundaries where possible
- Parsing failures are logged

### BB-015 - Holiday CSV ingestion

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the system, I want the 2026 holiday CSV ingested so that holiday answers can be deterministic.

**Acceptance Criteria**
- CSV can be loaded into the backend
- Holiday records preserve date, type, and region
- Basel-Stadt-specific holidays are identifiable

### BB-016 - Section-aware chunking

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want section-aware chunks so that retrieval and citation quality improve.

**Acceptance Criteria**
- Chunks are not created by naive fixed size only
- Chunk metadata includes section title
- Chunk sizes remain suitable for retrieval and generation

### BB-017 - Metadata enrichment

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want chunks enriched with metadata so that filtering and source display are reliable.

**Acceptance Criteria**
- Metadata includes document name
- Metadata includes section title or heading
- Metadata includes page number when available
- Metadata includes policy domain and sensitivity level

### BB-018 - Embedding generation and storage

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want embeddings stored for active chunks so that semantic search is possible.

**Acceptance Criteria**
- Embeddings are generated for chunked content
- Stored records link embeddings to chunk metadata
- Failed embedding jobs are detectable

### BB-019 - Knowledge base persistence

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want a queryable knowledge store so that relevant content can be retrieved quickly.

**Acceptance Criteria**
- PostgreSQL schema is created
- Vector storage is enabled
- Chunk records can be inserted and queried

## Epic 5: Retrieval and Grounding

### BB-020 - Semantic retrieval

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want to retrieve relevant chunks for a question so that answers are grounded in approved content.

**Acceptance Criteria**
- Retrieval returns top relevant chunks
- Returned chunks are limited to a safe number
- Results include metadata for citation and auditing

### BB-021 - Metadata-aware filtering

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want metadata filters so that results better match domain, sensitivity, and location.

**Acceptance Criteria**
- Retrieval can filter by policy domain
- Retrieval can filter by sensitivity or active status
- Retrieval supports location-specific content such as Basel-Stadt

### BB-022 - Retrieval quality evaluation

**Priority:** Should Have  
**Estimate:** M  
**Story:** As the team, we want retrieval checks so that we can detect weak grounding early.

**Acceptance Criteria**
- A small evaluation set exists
- Retrieval output can be inspected against expected sections
- Major mismatches are visible to the team

## Epic 6: Guardrails and High-Risk Validation

### BB-023 - Structured topic and response-type extraction

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want the structured LLM draft to expose topic and response-type signals so that backend validators can enforce safe behavior.

**Acceptance Criteria**
- Structured drafts include coarse topics such as expense, holiday, security, misconduct, or handbook-general
- Structured drafts include a response type such as policy answer, clarification, refusal, redirect, or verification failure
- Unsupported or unclear questions remain detectable through structured draft fields

### BB-024 - Expense rule enforcement

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the system, I must enforce expense rules deterministically so that policy violations are not answered incorrectly.

**Acceptance Criteria**
- Expenses above 35 CHF per person are rejected
- Alcohol-related expense requests are rejected
- Client lunch conditions can be reflected when relevant
- Response explains the rule clearly
- Validators use structured facts rather than brittle substring matching alone

### BB-025 - Holiday rule enforcement

**Priority:** Must Have  
**Estimate:** M  
**Story:** As an employee, I want correct holiday answers so that I can plan work accurately.

**Acceptance Criteria**
- National holidays are answered correctly
- Basel-Stadt rules for May 1 are answered correctly
- Holiday logic distinguishes national and cantonal cases
- Validators can detect contradiction between structured facts and generated holiday answers

### BB-026 - Sensitive IT refusal and safe redirection

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I must refuse unsafe IT and access questions so that sensitive information is protected.

**Acceptance Criteria**
- Questions about internal Wi-Fi credentials are refused
- Questions asking for guest Wi-Fi passwords are refused in MVP
- MAC address registration details are not disclosed
- Safe guidance can direct the user to Sarah Muller or IT for access help
- Safe refusal wording is allowed even when restricted terms such as `MAC address` appear in the response

### BB-027 - Misconduct and whistleblowing redirection

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the system, I want to redirect misconduct-related questions so that users are sent to the correct human process.

**Acceptance Criteria**
- Harassment-related queries are not handled as normal Q&A
- Whistleblowing-related queries are redirected to the ombudsman process
- Response language is safe and clear

### BB-028 - Low-confidence fallback behavior

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want to refuse when evidence is insufficient so that I do not guess.

**Acceptance Criteria**
- System can detect insufficient grounding
- Unsupported answers are replaced by fallback or refusal
- No fabricated citations are returned

### BB-028A - Post-generation validator pipeline

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want structured validators after draft generation so that unsafe or inconsistent outputs are blocked before release.

**Acceptance Criteria**
- Schema validation runs on every draft
- Citation validation runs on trusted answer types
- Disclosure validation blocks restricted technical disclosure
- Consistency validation checks high-risk rules such as expense and Basel holiday logic
- Response-type validation enforces refusal or redirect behavior where required

## Epic 7: LLM Integration and Answer Generation

### BB-029 - Prompt design for grounded answers

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want prompts optimized for grounded answers so that the model stays within trusted context.

**Acceptance Criteria**
- Prompt instructs the model to use only retrieved content
- Prompt includes refusal behavior
- Prompt supports structured outputs

### BB-029A - Constrained AI helper usage

**Priority:** Should Have  
**Estimate:** S  
**Story:** As the system, I want tightly scoped AI helper steps so that translation, normalization, or future multilingual/voice support can be added without changing core validation logic.

**Acceptance Criteria**
- AI helper usage is limited to allowed tasks such as translation, normalization, or transcription
- Helper steps return structured outputs
- Helper steps do not decide whether a draft is safe to release

### BB-030 - LLM integration for response generation

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want to generate answers from approved context so that users receive clear responses.

**Acceptance Criteria**
- Model can be called from the backend
- Retrieved context is passed into generation
- System can return a valid structured draft answer

### BB-031 - Citation-aware answer generation

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want answers linked to retrieved evidence so that trust and auditability are preserved.

**Acceptance Criteria**
- Generated responses include source references
- Citation identifiers match retrieved chunks
- Citations can be rendered by the frontend

### BB-031A - Retry and safe fallback handling

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want controlled retry and fallback behavior so that failed drafts do not become unsafe user-visible answers.

**Acceptance Criteria**
- Recoverable validation failures can trigger one stricter retry
- Irrecoverable failures return refusal, redirect, or verification-failure responses
- A failed draft is never released directly to the user

### BB-032 - Simple follow-up handling

**Priority:** Should Have  
**Estimate:** M  
**Story:** As an employee, I want limited follow-up support so that I can continue a short conversation.

**Acceptance Criteria**
- System supports basic clarification turns
- Follow-up questions do not break core safety rules
- Single-turn behavior remains reliable

## Epic 8: Security, Access, and Compliance

### BB-033 - Basic authenticated access

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the organization, we want authenticated access so that the assistant is not openly available.

**Acceptance Criteria**
- Only authenticated users with approved accounts can access the app
- Session handling is implemented at MVP level
- Unauthorized requests are rejected
- Login is required for all users
- Final provider/mechanism is implemented without relying on Google Workspace OIDC

### BB-034 - Basic role-aware access model

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the system, I want role-aware behavior so that access to features can be controlled.

**Acceptance Criteria**
- At least Employee and Admin roles are modeled
- Role information is stored and resolved in the application database
- Admin can view all employee chat histories
- Employee can view only their own chat history

### BB-035 - Secret and configuration management

**Priority:** Must Have  
**Estimate:** S  
**Story:** As a developer, I want secrets handled safely so that credentials are not exposed in code.

**Acceptance Criteria**
- Secrets are read from environment variables
- No credentials are hardcoded in the repository
- Setup instructions explain required secrets without revealing values

### BB-036 - Input validation and basic abuse prevention

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the system, I want validated input so that malformed or risky requests are handled safely.

**Acceptance Criteria**
- Input size and format are validated
- Obviously malformed requests are rejected
- Request handling fails safely

## Epic 9: Observability, Logging, and Auditability

### BB-037 - Structured request and response logging

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the team, we want structured logs so that we can debug issues and review behavior.

**Acceptance Criteria**
- Logs include request metadata
- Logs include draft-generation and validator outcomes
- Logs avoid storing sensitive content unnecessarily
- Chat history is persisted

### BB-038 - Audit trail for answer generation

**Priority:** Must Have  
**Estimate:** M  
**Story:** As the team, we want an audit trail so that incorrect answers can be investigated.

**Acceptance Criteria**
- Retrieved chunk references are traceable
- Validator outcomes are recorded
- Refusal reasons can be inspected
- Admin can review all stored chat transcripts and related metadata

### BB-039 - Error monitoring basics

**Priority:** Could Have  
**Estimate:** S  
**Story:** As the team, we want basic error visibility so that failures are caught quickly.

**Acceptance Criteria**
- Critical backend errors are visible in logs
- Frontend error cases can be identified

## Epic 10: Quality Assurance and Evaluation

### BB-040 - Golden question set

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the team, we want a golden test set so that critical business behavior can be validated repeatedly.

**Acceptance Criteria**
- Golden questions cover expenses, holidays, general policy, and sensitive topics
- Expected behavior is defined for each question
- Test set is accessible to the team

### BB-041 - Unit tests for deterministic rules

**Priority:** Must Have  
**Estimate:** S  
**Story:** As a developer, I want rule tests so that critical business logic remains correct.

**Acceptance Criteria**
- Expense rule tests exist
- Holiday logic tests exist
- Failing rule behavior is detectable automatically

### BB-042 - Integration tests for `/ask` flow

**Priority:** Should Have  
**Estimate:** M  
**Story:** As the team, we want integration tests so that the main request pipeline stays stable.

**Acceptance Criteria**
- Tests cover a successful grounded answer
- Tests cover deterministic rule rejection
- Tests cover refusal for sensitive topics

### BB-043 - Manual QA checklist for demos and release

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the team, we want a manual QA checklist so that demo quality is consistent.

**Acceptance Criteria**
- Checklist includes critical scenarios
- Checklist includes citation verification
- Checklist includes refusal behavior verification

### BB-044 - AI evaluation scorecard

**Priority:** Should Have  
**Estimate:** M  
**Story:** As the team, we want an evaluation scorecard so that answer quality can be tracked over time.

**Acceptance Criteria**
- Scorecard tracks accuracy, source validity, safety, and consistency
- Review process is defined
- Results can be compared across iterations

## Epic 11: Deployment and Demo Readiness

### BB-045 - Demo-ready seed data and examples

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the team, we want predictable demo data so that stakeholder reviews run smoothly.

**Acceptance Criteria**
- Demo scenarios are prepared
- Required data files are available
- Known expected outputs are documented

### BB-046 - MVP deployment setup

**Priority:** Should Have  
**Estimate:** M  
**Story:** As the team, we want a deployable MVP so that the product can be demonstrated outside local machines.

**Acceptance Criteria**
- Frontend and backend can be deployed in a basic environment
- Environment-specific configuration is documented
- Deployment steps are repeatable

### BB-047 - Release checklist

**Priority:** Should Have  
**Estimate:** S  
**Story:** As the team, we want a release checklist so that delivery is controlled and predictable.

**Acceptance Criteria**
- Checklist includes testing, documentation, and risk review
- Checklist includes sign-off responsibilities

## Epic 12: Documentation and Team Enablement

### BB-048 - Technical architecture documentation

**Priority:** Must Have  
**Estimate:** S  
**Story:** As the team, we want architecture documented so that implementation decisions stay aligned.

**Acceptance Criteria**
- Component responsibilities are documented
- Request flow is documented
- Data flow and guardrail points are visible

### BB-049 - Developer onboarding guide

**Priority:** Should Have  
**Estimate:** S  
**Story:** As a new team member, I want onboarding guidance so that I can become productive quickly.

**Acceptance Criteria**
- Setup steps are documented
- Key folders and responsibilities are described
- Common commands are listed

### BB-050 - Admin and stakeholder demo guide

**Priority:** Could Have  
**Estimate:** S  
**Story:** As the project team, we want a demo script so that stakeholder presentations stay focused on value and risk controls.

**Acceptance Criteria**
- Demo shows expense rejection
- Demo shows Basel holiday accuracy
- Demo shows sensitive-topic refusal
- Demo shows source-backed answer

## Won't Have for This Phase

- Payroll or salary change workflows
- Full HR case management
- Logistics tracking or warehouse operations support
- Open self-service disclosure of Wi-Fi credentials through the bot
- Exposure of internal technical identifiers or device registration details
- Advanced analytics dashboard
- Slack-first or Teams-first rollout
- Real-time enterprise system integrations
- Autonomous workflow execution

## Optional Post-MVP Enhancements

- voice message input with speech-to-text before the existing text pipeline
- receipt upload with OCR
- stronger RBAC and admin tooling
- analytics and reporting

The preferred design for future voice support is a modular `voice input adapter` that feeds the existing text-first pipeline.

## Suggested MVP Cut Line

The following items form the recommended MVP scope for a 3-week, 5-person team:

- BB-001 to BB-007
- BB-009 to BB-021
- BB-023 to BB-031A
- BB-033 to BB-038
- BB-040 to BB-043
- BB-045
- BB-048

Items such as final authentication choice and logging retention policy require clarification before they should be treated as committed MVP scope.

## Suggested Delivery Sequence

### Week 1

- Foundation, API skeleton, UI shell
- Handbook parsing and holiday CSV loading
- Shared contracts
- Basic retrieval and structured draft generation

### Week 2

- Validator pipeline and fallback handling
- Source citation
- Basel holiday logic
- Sensitive-topic refusal and consistency checks
- End-to-end integration

### Week 3

- QA hardening
- Golden question evaluation
- Bug fixing
- Documentation
- Demo and release readiness

## Notes

- All stories should satisfy the Definition of Ready before sprint commitment.
- All completed work should satisfy the Definition of Done, including safety, source validation, and testing expectations.
- If time becomes tight, prefer cutting optional UX polish and access-control depth before cutting core rule accuracy, source grounding, or refusal safety.
