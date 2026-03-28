## 6. End-to-End Request Flow

### Step 1: User submits a question

The user enters a question into the custom web interface.

**Example:**  
“Can I expense a 36 CHF lunch?”

---

### Step 2: API receives the request

The backend receives the question and validates:

- authentication
- session
- input format
- basic request integrity

---

### Step 3: Query classification runs

The system classifies the query into a policy domain and determines whether it is likely:

- answerable via retrieval
- deterministic
- sensitive
- unsupported

---

### Step 4: Policy decision layer evaluates the request

The system checks:

- Is this a hard-rule scenario?
- Is the query restricted?
- Should this be refused or redirected?
- Is the question eligible for LLM-based answering?

For example:

- An expense question with 36 CHF should be handled deterministically.
- A request for internal credentials should be refused.
- A harassment-related question should be redirected rather than answered through general Q&A. The handbook explicitly states that harassment, bullying, and whistleblowing matters should not be discussed with the internal bot and should instead go to the external confidential ombudsman. :contentReference[oaicite:0]{index=0}

---

### Step 5A: Deterministic answer path

If the query matches a known business rule, the system answers through rule logic.

**Examples:**

- Expense above 35 CHF → reject
- Alcohol included → reject
- Unsafe request → refuse

This path does not depend on probabilistic reasoning.

---

### Step 5B: Retrieval path

If the question requires document-supported explanation, the system:

- retrieves relevant chunks
- filters by domain and metadata
- passes only top-ranked context onward

---

### Step 6: LLM generation

The LLM receives:

- the user question
- the approved retrieved context
- system rules for output format
- constraints against unsupported guessing

The model then produces a structured response.

---

### Step 7: Response validation

The backend validates:

- that citations exist
- that citation references match retrieved chunks
- that the output format is valid
- that refusal logic is respected
- that no restricted content is exposed

---

### Step 8: Response returned to UI

The user receives:

- a clear answer
- source references
- refusal/redirection if necessary

---

### Step 9: Audit trail recorded

All relevant metadata is stored for:

- debugging
- QA review
- regression evaluation
- stakeholder demonstrations

---

## 7. Component Responsibilities in Detail

### 7.1 Frontend Responsibilities

The frontend should:

- provide a simple chat-like interaction
- render citations clearly
- differentiate between:
  - standard answers
  - refusals
  - redirections
- handle errors gracefully
- remain lightweight in MVP

---

### 7.2 Backend Responsibilities

The backend should:

- act as the single orchestration layer
- centralize decision flow
- prevent direct UI-to-model coupling
- encapsulate security, retrieval, and validation logic

This is essential for maintaining control over trust and compliance behavior.

---

### 7.3 Knowledge Base Responsibilities

The knowledge base must:

- store chunked source content
- preserve source metadata
- support retrieval by relevance and filters
- distinguish content by version and sensitivity

---

## 8. Data Model Concept

Each document chunk should include at least the following fields:

- `chunk_id`
- `document_name`
- `document_version`
- `section_title`
- `page_number`
- `chunk_text`
- `embedding`
- `policy_domain`
- `location_scope`
- `audience`
- `sensitivity_level`
- `is_active`

This is important because the handbook contains content that varies by domain and sensitivity, including holiday rules, expenses, security, and sensitive misconduct guidance. :contentReference[oaicite:1]{index=1}

---

## 9. Document Ingestion Design

### 9.1 Source Types

Initial MVP sources:

- Employee Handbook
- Structured business rule supplements
- Approved holiday logic source

The stakeholder brief includes Basel-specific holiday expectations and a structured holiday logic example, including Labor Day on May 1st for Basel-Stadt only. :contentReference[oaicite:2]{index=2}

---

### 9.2 Ingestion Steps

1. Parse PDF or structured source
2. Detect section boundaries
3. Chunk content by semantic section
4. Attach metadata
5. Generate embeddings
6. Store in knowledge base

---

### 9.3 Chunking Strategy

The system should use **section-aware chunking**, not naive fixed-size chunking.

Preferred examples:

- 4. Time Off (Vacation & Holidays)
- 6. IT, Security & Connectivity
- 7. Expenses & Travel
- 9. Sensitive Matters & Conduct

This improves:

- retrieval quality
- citation quality
- explainability

---

## 10. Security Architecture

### 10.1 Security Objectives

The system must:

- protect sensitive internal information
- prevent misuse
- restrict disclosures based on topic and role
- fail safely when uncertain

---

### 10.2 Security Controls

Recommended controls:

- authenticated access only
- RBAC
- input validation
- sensitive topic detection
- refusal/redirection layer
- server-side logging
- secret management for infrastructure

---

### 10.3 Sensitive Topic Handling

Sensitive topics must be explicitly classified.

Example categories:

- internal credentials
- MAC/device registration details
- serious misconduct
- whistleblowing
- confidential HR matters

The handbook and stakeholder brief both indicate that not all internal information should be disclosed freely. The stakeholder explicitly requires that internal Wi-Fi passwords or MAC address details not be given out “to just anyone.” :contentReference[oaicite:3]{index=3}

---

## 11. Reliability & Safety Controls

The architecture includes the following safety mechanisms:

- Rule-first evaluation for deterministic cases
- Retrieval before generation
- Approved-source-only answering
- Refusal when evidence is insufficient
- Citation validation
- Audit logging
- Regression testing with golden questions

---

## 12. Non-Functional Architectural Qualities

### Accuracy

Achieved through:

- domain-aware retrieval
- deterministic rule engine
- source-backed generation

### Security

Achieved through:

- authentication
- authorization
- sensitive-topic filtering
- refusal behavior

### Maintainability

Achieved through:

- modular service boundaries
- structured response contracts
- independent ingestion and retrieval layers

### Auditability

Achieved through:

- full request logging
- source traceability
- document version tracking

### Extensibility

The architecture can later support:

- more source documents
- admin dashboards
- analytics
- additional communication channels
- advanced review workflows

---

## 13. Deployment View (MVP)

### Frontend

- Hosted as a web application

### Backend

- Hosted as a containerized API service

### Database

- PostgreSQL with pgvector extension

### External Services

- LLM / embedding provider
- optional identity provider

---

## 14. MVP Architectural Constraints

For the first project phase, the architecture intentionally excludes:

- complex microservices decomposition
- event-driven architecture
- real-time external integrations
- autonomous workflow execution
- broad enterprise system connectivity

This is deliberate to keep the MVP focused, testable, and deliverable within the available timeline.

---

## 15. Architectural Risks

### Risk 1: Weak retrieval quality

**Impact:** Incorrect or incomplete answers  
**Mitigation:** Metadata-aware retrieval, golden question testing, chunk strategy refinement

### Risk 2: Policy violations through generation

**Impact:** Loss of trust and possible rejection by stakeholder  
**Mitigation:** Rule-first policy layer, output validation, refusal mechanisms

### Risk 3: Unsafe disclosure of internal information

**Impact:** Security breach  
**Mitigation:** Sensitive topic classification, authorization, response filtering

### Risk 4: Over-engineering MVP

**Impact:** Delayed delivery  
**Mitigation:** Single orchestrator backend, minimal number of services, focused scope

---

## 16. Architectural Principles

The system must follow these principles:

- **Policy before language generation**
- **Grounded answers only**
- **Trust over convenience**
- **Secure by default**
- **Simple architecture, strong controls**
- **Human escalation for sensitive cases**

---

## 17. Decision Statement

The target architecture for Beat-Bot is a **modular, web-based, policy-aware RAG system** with deterministic rule enforcement, controlled LLM usage, and full source traceability.

This architecture is appropriate for the problem because the product must behave as a **trusted policy assistant**, not as a generic conversational AI tool.
