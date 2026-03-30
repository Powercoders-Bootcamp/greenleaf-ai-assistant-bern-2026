# Product Backlog

## GreenLeaf Logistics - Beat-Bot

## 1. Product Goal

Deliver a trusted internal AI assistant that answers employee policy questions from approved sources, enforces critical business rules, and refuses or redirects unsafe requests.

## 2. Delivery Assumptions

- Team size: `6 people`
- Delivery window: `3 weeks`
- MVP access model: authenticated users only
- MVP roles: `Employee`, `Admin`
- Current architecture: `LLM-first + structured draft + validators + safe fallback`
- Current input model: `text only`
- Current language scope: `no multilingual support in MVP`
- Current voice scope: `out of MVP`

## 3. Scrum Structure

This backlog is organized as:

- `Epic`
- `Product Backlog Item (PBI)`
- `User Story or Technical Story`
- `Acceptance Criteria`
- `Priority`
- `Estimate`
- `Dependencies`

## 4. Priority Scale

- `Must Have`
- `Should Have`
- `Could Have`
- `Won't Have`

## 5. Estimation Scale

- `S`
- `M`
- `L`

## 6. Epics

- `E1` Product Foundation
- `E2` User Interface
- `E3` Core Ask Flow
- `E4` Source Ingestion and Retrieval
- `E5` Validation and Guardrails
- `E6` Authentication, Roles, and History
- `E7` Quality and Release

## 7. Product Backlog Items

### E1 - Product Foundation

#### PBI-001 - Repository and Team Conventions

**Story**  
As a `project team`, we want a clear repo structure and working conventions so that development stays consistent.

**Business Value**  
Reduces coordination overhead and setup confusion.

**Acceptance Criteria**

- repository structure is documented
- branching and PR conventions are documented
- ownership and working agreements are visible

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** None

#### PBI-002 - Local Development Environment

**Story**  
As a `developer`, I want a working local setup so that I can contribute without setup blockers.

**Business Value**  
Allows the team to start implementation quickly.

**Acceptance Criteria**

- frontend runs locally
- backend runs locally
- required environment variables are documented
- local setup instructions are available

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-001

#### PBI-003 - Shared Contracts

**Story**  
As a `team`, we want shared request and response contracts so that frontend and backend integrate cleanly.

**Business Value**  
Prevents integration mismatch and rework.

**Acceptance Criteria**

- ask request schema is defined
- response schema is defined
- error schema is defined
- example payloads are documented

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-002

### E2 - User Interface

#### PBI-004 - Basic Chat Interface

**Story**  
As an `Employee`, I want a simple chat interface so that I can ask policy questions easily.

**Business Value**  
Provides the main employee-facing value of the product.

**Acceptance Criteria**

- user can type and submit a question
- conversation area shows user and assistant messages
- layout works on desktop and mobile

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-003

#### PBI-005 - Loading and Error States

**Story**  
As an `Employee`, I want clear feedback while the system is working so that the experience feels reliable.

**Business Value**  
Improves usability and trust.

**Acceptance Criteria**

- loading state is visible
- backend/network errors are visible
- invalid input is handled safely

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-004

#### PBI-006 - Citation Display

**Story**  
As an `Employee`, I want to see the source of an answer so that I can verify it myself.

**Business Value**  
Improves trust and reduces policy disputes.

**Acceptance Criteria**

- answers can display citations
- citation format is human-readable
- citation can show document, section, and page when available

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-004, PBI-021

#### PBI-007 - Refusal and Redirect UI

**Story**  
As an `Employee`, I want refusals and redirects to be clearly shown so that I know what to do next.

**Business Value**  
Makes sensitive-topic handling understandable instead of confusing.

**Acceptance Criteria**

- refusal responses are distinguishable from normal answers
- redirect responses clearly show the next step
- restricted content is not exposed in the UI

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-004, PBI-027

### E3 - Core Ask Flow

#### PBI-008 - API Skeleton and Health Check

**Story**  
As a `developer`, I want a working API skeleton so that the backend can be integrated safely.

**Business Value**  
Creates the base for all backend delivery.

**Acceptance Criteria**

- backend starts successfully
- health endpoint exists
- base routing structure exists

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-002

#### PBI-009 - `/ask` Endpoint

**Story**  
As the `frontend`, I want a stable `/ask` endpoint so that user questions can be submitted to the backend.

**Business Value**  
Connects the UI to the assistant logic.

**Acceptance Criteria**

- endpoint accepts validated ask payload
- endpoint returns structured response
- invalid input returns safe error output

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-008, PBI-003

#### PBI-010 - Ask Orchestration Flow

**Story**  
As the `System`, I want one orchestration flow so that retrieval, draft generation, validation, and fallback happen consistently.

**Business Value**  
Makes backend behavior predictable and maintainable.

**Acceptance Criteria**

- retrieval is called before answer drafting
- the LLM returns a structured draft
- validators run before any user-visible response
- retry/fallback behavior is centralized

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-009, PBI-018, PBI-020, PBI-024

#### PBI-011 - Structured Draft Generation

**Story**  
As the `System`, I want the LLM to return structured drafts so that the backend can validate them safely.

**Business Value**  
Reduces reliance on brittle raw-text checks.

**Acceptance Criteria**

- draft includes `answer_text`
- draft includes `response_type`
- draft includes `decision`
- draft includes `citations` when applicable
- draft includes structured facts when available

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-020, PBI-021

#### PBI-012 - Final Response Formatting

**Story**  
As an `Employee`, I want clear final responses so that I can understand the answer quickly.

**Business Value**  
Improves usability and reduces ambiguity.

**Acceptance Criteria**

- final response separates answer from citations
- fallback/refusal/redirect responses are formatted clearly
- frontend-ready response payload is returned

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-011, PBI-024

### E4 - Source Ingestion and Retrieval

#### PBI-013 - Approved Source Inventory

**Story**  
As the `team`, we want a defined list of approved sources so that the assistant answers only from trusted content.

**Business Value**  
Protects trust and narrows scope.

**Acceptance Criteria**

- approved source list is documented
- each source has a version or date reference
- out-of-scope sources are excluded

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** None

#### PBI-014 - Handbook Parsing

**Story**  
As the `System`, I want to parse the handbook so that it can be searched and cited.

**Business Value**  
Makes handbook Q&A possible.

**Acceptance Criteria**

- handbook PDF can be parsed
- section structure is preserved where possible
- parsing failures are logged

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-013

#### PBI-015 - Holiday CSV Ingestion

**Story**  
As the `System`, I want to load the holiday CSV so that holiday answers can use trusted data.

**Business Value**  
Supports Basel holiday correctness.

**Acceptance Criteria**

- CSV loads successfully
- date, type, and region fields are preserved
- Basel-Stadt rules are identifiable

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-013

#### PBI-016 - Chunking and Metadata Enrichment

**Story**  
As the `System`, I want section-aware chunks with metadata so that retrieval and citation quality improve.

**Business Value**  
Improves grounding quality and traceability.

**Acceptance Criteria**

- chunks preserve section boundaries where practical
- metadata includes document, section, and page when available
- chunks remain retrieval-friendly in size

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-014

#### PBI-017 - Knowledge Store Persistence

**Story**  
As the `System`, I want source data stored in PostgreSQL plus pgvector so that retrieval can run efficiently.

**Business Value**  
Provides one practical store for app data and retrieval data.

**Acceptance Criteria**

- DB schema exists for source documents and chunks
- vector storage is enabled
- chunk records can be inserted and queried

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-016

#### PBI-018 - Embeddings and Semantic Retrieval

**Story**  
As the `System`, I want to retrieve relevant chunks for a question so that answers are grounded in approved sources.

**Business Value**  
Enables source-backed LLM responses.

**Acceptance Criteria**

- embeddings are generated and stored
- retrieval returns top relevant chunks
- retrieval output includes citation metadata

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-017

### E5 - Validation and Guardrails

#### PBI-019 - Citation Validation

**Story**  
As the `System`, I want trusted answer types to require citations so that unsupported policy answers are not released.

**Business Value**  
Preserves trust and auditability.

**Acceptance Criteria**

- policy-style answers require citations
- invalid or missing citations trigger retry or fallback
- citation validation outcome is traceable

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-011

#### PBI-020 - Disclosure Validation

**Story**  
As the `System`, I want to block restricted technical disclosure so that sensitive access details are not leaked.

**Business Value**  
Protects sponsor trust and safety boundaries.

**Acceptance Criteria**

- internal Wi-Fi password responses are blocked
- guest Wi-Fi password responses are blocked in MVP
- actionable MAC registration details are blocked
- safe refusal wording is still allowed

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-011

#### PBI-021 - Consistency Validation

**Story**  
As the `System`, I want high-risk business rules checked against structured facts so that incorrect outputs are blocked.

**Business Value**  
Reduces risk on critical sponsor scenarios.

**Acceptance Criteria**

- expense consistency checks exist
- Basel holiday consistency checks exist
- validators prefer structured facts over brittle string matching

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-011, PBI-015

#### PBI-022 - Response-Type Validation

**Story**  
As the `System`, I want refusal and redirect behavior enforced so that sensitive topics do not return the wrong answer type.

**Business Value**  
Makes misconduct and IT safety behavior dependable.

**Acceptance Criteria**

- Wi-Fi and MAC topics produce refusal behavior
- misconduct topics produce redirect behavior
- invalid response types trigger retry or fallback

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-011

#### PBI-023 - Retry and Safe Fallback

**Story**  
As the `System`, I want retry and safe fallback handling so that failed drafts do not become unsafe user-visible answers.

**Business Value**  
Provides safe degradation when the model output is weak.

**Acceptance Criteria**

- recoverable failures can trigger one stricter retry
- irrecoverable failures return refusal, redirect, or verification failure
- failed drafts are never released directly

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-019, PBI-020, PBI-021, PBI-022

### E6 - Authentication, Roles, and History

#### PBI-024 - Authenticated Access

**Story**  
As the `organization`, we want authenticated access so that the assistant is not openly available.

**Business Value**  
Protects internal use and enables role-based features.

**Acceptance Criteria**

- login is required
- unauthorized requests are rejected
- session or token handling works at MVP level
- chosen auth mechanism is implemented without relying on Google Workspace OIDC

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-008

#### PBI-025 - Role Model and Access Checks

**Story**  
As the `System`, I want Employee and Admin roles enforced so that data access follows product rules.

**Business Value**  
Supports admin review without exposing other employees’ data broadly.

**Acceptance Criteria**

- Employee and Admin roles exist
- role mapping is stored in the application database
- route-level access checks work

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-024

#### PBI-026 - Chat History Persistence

**Story**  
As an `Employee`, I want my chat history saved so that I can review previous assistant answers.

**Business Value**  
Improves continuity and traceability.

**Acceptance Criteria**

- chats and messages are stored in the application database
- each employee can view only their own history
- related metadata is persisted

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-025, PBI-009

#### PBI-027 - Admin Chat Review

**Story**  
As an `Admin`, I want to review all employee chat histories and metadata so that I can investigate system behavior.

**Business Value**  
Supports operational review and QA.

**Acceptance Criteria**

- admin can view all employee chat histories
- admin can inspect related metadata
- employee restrictions remain enforced for non-admins

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-026

#### PBI-028 - Secrets and Config Management

**Story**  
As a `developer`, I want secrets managed safely so that credentials are not exposed in code.

**Business Value**  
Supports secure delivery and safer collaboration.

**Acceptance Criteria**

- secrets come from environment variables
- no credentials are hardcoded
- required secrets are documented safely

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-002

### E7 - Quality and Release

#### PBI-029 - Structured Logs and Audit Trail

**Story**  
As the `team`, we want logs and traceability so that failures can be debugged and investigated.

**Business Value**  
Supports QA, demo safety, and admin review.

**Acceptance Criteria**

- logs include request metadata
- logs include draft-generation and validator outcomes
- logs avoid storing unnecessary sensitive content
- retrieval trace is inspectable

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-023, PBI-026

#### PBI-030 - Golden Question Set

**Story**  
As the `team`, we want a golden test set so that critical business behavior can be verified repeatedly.

**Business Value**  
Prevents regressions on the most important scenarios.

**Acceptance Criteria**

- golden questions cover expenses, holidays, general policy, and sensitive topics
- expected outcomes are defined
- test set is accessible to the team

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** None

#### PBI-031 - Core Automated and Manual QA

**Story**  
As the `team`, we want tests and a QA checklist so that MVP quality is consistent.

**Business Value**  
Improves release confidence.

**Acceptance Criteria**

- expense and holiday checks are tested
- ask-flow integration is covered at MVP level
- manual QA checklist exists for demos and release

**Priority:** Must Have  
**Estimate:** M  
**Dependencies:** PBI-030, PBI-021, PBI-023

#### PBI-032 - Demo Readiness

**Story**  
As the `team`, we want a demo-ready MVP so that stakeholder reviews clearly show product value and safety.

**Business Value**  
Increases delivery confidence and stakeholder buy-in.

**Acceptance Criteria**

- demo scenarios are prepared
- expected outcomes are documented
- core MVP flows work end-to-end

**Priority:** Must Have  
**Estimate:** S  
**Dependencies:** PBI-031

## 8. Definition of Ready

A PBI is ready when:

- story text is clear
- business value is understood
- acceptance criteria are testable
- dependencies are known
- open blockers are visible
- estimate is agreed

## 9. Definition of Done

A PBI is done when:

- acceptance criteria are met
- code is reviewed
- tests or validation checks are completed
- security expectations are satisfied
- citations and fallback behavior work where relevant
- documentation is updated if needed

## 10. Suggested Sprint Breakdown

### Sprint 1

- PBI-001 to PBI-010
- PBI-013 to PBI-018
- PBI-024
- PBI-028
- PBI-030

### Sprint 2

- PBI-011 to PBI-023
- PBI-025
- PBI-026

### Sprint 3

- PBI-027
- PBI-029
- PBI-031
- PBI-032
- bug fixing and hardening

## 11. MVP Cut Line

Recommended MVP PBIs:

- PBI-001 to PBI-012
- PBI-013 to PBI-023
- PBI-024 to PBI-029
- PBI-030 to PBI-032

## 12. Won't Have in This Phase

- payroll or salary workflows
- full HR case management
- logistics tracking support
- self-service disclosure of Wi-Fi credentials
- MAC registration detail disclosure
- voice input
- multilingual support
- OCR receipt upload

## 13. Current Major Risks

- weak retrieval quality
- unsafe or uncited LLM drafts
- incorrect expense validation
- incorrect Basel holiday handling
- sensitive IT disclosure
- scope creep in a 3-week delivery window
