# Target Architecture

## GreenLeaf Logistics – Beat-Bot

---

## 1. Purpose

This document defines the target system architecture for the Beat-Bot MVP.

It explains:

- The major system components
- Their responsibilities
- The end-to-end request flow
- Security and policy enforcement points
- Architectural constraints and design principles

The target architecture is designed to support a **trusted internal policy assistant** rather than a general-purpose chatbot. This distinction is critical because the stakeholder requires strict policy accuracy, Basel-specific holiday handling, protection of sensitive information, and proof of source in every trustworthy answer. :contentReference[oaicite:0]{index=0}

---

## 2. Architectural Goal

The goal of the architecture is to deliver a system that is:

- **Accurate** in answering policy-related questions
- **Grounded** in approved internal sources
- **Deterministic** where rules are explicit
- **Secure** in handling sensitive topics
- **Auditable** in its reasoning path and outputs
- **Simple enough** for MVP delivery, but extensible for future iterations

---

## 3. Architectural Style

The Beat-Bot follows a **modular web-based RAG architecture with rule-based policy enforcement**.

This means:

- Users interact through a custom web UI
- The backend orchestrates retrieval, rules, and answer generation
- Approved documents are ingested into a searchable knowledge base
- A policy layer handles deterministic and sensitive decisions
- The LLM is used only where retrieval and rules allow it

This architectural style is intentionally chosen to reduce hallucination risk and enforce trust boundaries.

---

## 4. High-Level System Components

### 4.1 Presentation Layer

**Technology:** Next.js + TypeScript

**Responsibilities:**

- User login and session handling
- Question input
- Response rendering
- Citation display
- Refusal/fallback display
- Admin-facing visibility for controlled review in later phases

---

### 4.2 API / Orchestration Layer

**Technology:** FastAPI (Python)

**Responsibilities:**

- Accept and validate incoming requests
- Coordinate downstream services
- Trigger policy and security checks
- Trigger retrieval and answer generation
- Return structured responses to the UI
- Log requests and outputs

---

### 4.3 Authentication & Authorization Layer

**Technology:** Email-based login or OIDC provider

**Responsibilities:**

- Authenticate users
- Assign roles (e.g., Employee, Admin)
- Enforce role-based access rules
- Ensure only authorized users can use protected features

---

### 4.4 Query Classification Layer

**Responsibilities:**

- Detect the likely business domain of the question
- Identify whether the question is:
  - informational
  - rule-based
  - sensitive
  - unsupported
- Route the query appropriately

**Example domains:**

- Expenses
- Holidays
- Leave
- Attendance
- IT/Security
- Sensitive Conduct

---

### 4.5 Policy Decision Layer

**Responsibilities:**

- Evaluate hard business rules
- Detect restricted topics
- Trigger refusal or redirect logic
- Decide whether a question should:
  - be answered deterministically
  - be answered through retrieval + LLM
  - be refused
  - be escalated

This is a critical component because some requirements must never depend on probabilistic interpretation. For example, handbook rules explicitly define that client lunches are reimbursable only under certain conditions, that the maximum is 35 CHF per person, and that alcohol is not reimbursable. :contentReference[oaicite:1]{index=1}

---

### 4.6 Retrieval Layer

**Technology:** PostgreSQL + pgvector + metadata filtering

**Responsibilities:**

- Retrieve the most relevant content chunks from approved sources
- Apply metadata filters such as:
  - section
  - topic
  - sensitivity
  - location scope
  - document version
- Rank and return the most relevant chunks

---

### 4.7 LLM Response Generation Layer

**Technology:** OpenAI API

**Responsibilities:**

- Generate answers using only retrieved context
- Produce structured outputs
- Avoid unsupported synthesis
- Respect refusal and answer constraints from upstream layers

**Required output structure:**

- answer
- citations
- confidence
- refusal_flag
- escalation_target
- policy_rule_applied

---

### 4.8 Knowledge Ingestion Layer

**Responsibilities:**

- Parse approved documents
- Split them into semantically useful chunks
- Enrich chunks with metadata
- Generate embeddings
- Store chunks in the knowledge base

---

### 4.9 Audit & Logging Layer

**Responsibilities:**

- Log every request and response lifecycle
- Store:
  - user role
  - query
  - classification result
  - rules triggered
  - retrieved chunks
  - generated answer
  - refusal reason
  - document version
- Support evaluation, debugging, and incident review

---

## 5. High-Level Architecture Diagram (Logical View)

```text
+----------------------+
|      Web UI          |
|  (Next.js Frontend)  |
+----------+-----------+
           |
           v
+----------------------+
|   API / Orchestrator |
|   (FastAPI Backend)  |
+----------+-----------+
           |
           v
+----------------------+        +----------------------+
| Authentication /     |        |   Audit & Logging    |
| Authorization Layer  |        |      Layer           |
+----------------------+        +----------------------+
           |
           v
+----------------------+
| Query Classification |
+----------+-----------+
           |
           v
+----------------------+
| Policy Decision Layer|
+----+------------+----+
     |            |
     |            +--------------------------+
     |                                       |
     v                                       v
+----------------------+        +----------------------+
| Deterministic Rules  |        |  Retrieval Layer     |
| (hard-coded logic)   |        | (Postgres + pgvector)|
+----------------------+        +----------+-----------+
                                           |
                                           v
                                +----------------------+
                                | LLM Response Engine  |
                                +----------+-----------+
                                           |
                                           v
                                +----------------------+
                                | Structured Response  |
                                +----------+-----------+
                                           |
                                           v
                                +----------------------+
                                |      Web UI          |
                                +----------------------+
```
