# User Stories Backlog

## GreenLeaf Logistics – Beat-Bot

---

## 1. Purpose

This document defines the **prioritized and refined user stories backlog** for the Beat-Bot project.

It is structured to:

- Support Agile sprint planning
- Feed the GitHub Kanban board
- Align development with business priorities

---

## 2. User Roles

- **Employee** – primary user asking questions
- **Admin** – stakeholder ensuring accuracy and compliance
- **IT & Security** – ensures safe system behavior
- **System** – enforces technical and policy constraints

---

## 3. Backlog Structure

Each user story includes:

- Role
- Goal
- Benefit
- Acceptance Criteria

---

## 4. MUST HAVE (Sprint 1 Priority)

### Epic: Core Q&A Functionality

#### US-001

**As an Employee, I want to ask a question in natural language so that I can quickly get information.**

**Acceptance Criteria:**

- User can input text query
- System processes and returns a response
- Response is displayed clearly in UI

---

#### US-002

**As an Employee, I want to receive accurate answers based on the handbook so that I can trust the system.**

**Acceptance Criteria:**

- Answers are based only on approved sources
- No hallucinated information
- System refuses when unsure

---

#### US-003

**As an Employee, I want to see the source of each answer so that I can verify the information.**

**Acceptance Criteria:**

- Source section/page is displayed
- Source matches retrieved content
- Source is human-readable

---

---

### Epic: Policy Enforcement

#### US-004

**As the System, I must reject expenses above 35 CHF so that company rules are enforced.**

**Acceptance Criteria:**

- Input containing >35 CHF → rejected
- Clear explanation provided
- No ambiguity in response

---

#### US-005

**As the System, I must reject expenses involving alcohol so that policy violations are prevented.**

**Acceptance Criteria:**

- Alcohol detected → automatic rejection
- Explanation references policy

---

#### US-006

**As an Employee, I want to know if a date is a holiday so that I can plan my work.**

**Acceptance Criteria:**

- Correct holiday returned
- Basel-specific logic applied
- Distinction between national and cantonal holidays

---

---

### Epic: Security & Safety

#### US-007

**As the System, I must prevent disclosure of sensitive information so that security is maintained.**

**Acceptance Criteria:**

- Sensitive queries are detected
- System refuses or limits response
- No credentials or internal details exposed

---

#### US-008

**As an Employee, I want the system to safely handle unknown questions so that I am not misinformed.**

**Acceptance Criteria:**

- System refuses when confidence is low
- Safe fallback message shown
- No fabricated answers

---

---

### Epic: Basic System Infrastructure

#### US-009

**As a Developer, I want a working API endpoint so that the frontend can communicate with the backend.**

**Acceptance Criteria:**

- `/ask` endpoint implemented
- Returns structured response
- Handles errors gracefully

---

#### US-010

**As a Developer, I want the handbook ingested into a searchable system so that questions can be answered.**

**Acceptance Criteria:**

- PDF parsed into chunks
- Metadata stored (section, page)
- Embeddings generated and stored

---

#### US-011

**As the System, I must retrieve relevant information before answering so that responses are grounded.**

**Acceptance Criteria:**

- Retrieval returns relevant chunks
- Limited number of chunks passed to model
- Irrelevant content filtered out

---

---

## 5. SHOULD HAVE (Next Priority)

### Epic: Usability & Clarity

#### US-012

**As an Employee, I want clear and concise answers so that I understand policies easily.**

---

#### US-013

**As an Employee, I want answers formatted in a structured way so that they are easy to read.**

---

#### US-014

**As an Admin, I want consistent answers so that employees receive reliable information.**

---

---

### Epic: Observability

#### US-015

**As a Developer, I want to log queries and responses so that I can debug issues.**

---

#### US-016

**As an Admin, I want visibility into system behavior so that I can monitor performance.**

---

---

## 6. COULD HAVE (Optional Enhancements)

### Epic: UX Enhancements

#### US-017

**As an Employee, I want a friendly conversational interface so that the experience feels natural.**

---

#### US-018

**As an Employee, I want suggested follow-up questions so that I can explore further.**

---

### Epic: Admin Features

#### US-019

**As an Admin, I want a dashboard to review usage so that I understand system impact.**

---

---

## 7. WON’T HAVE (Out of Scope)

- Salary or compensation processing
- Logistics tracking
- HR case management
- Access to confidential credentials
- Full enterprise integrations

---

## 8. Backlog Prioritization Summary

| Priority | Focus Area            |
| -------- | --------------------- |
| MUST     | Core Q&A + Safety     |
| SHOULD   | UX + Observability    |
| COULD    | Enhancements          |
| WON’T    | Out of Scope Features |

---

## 9. Sprint 1 Candidate Stories

Recommended for Sprint 1:

- US-001 → Basic UI input/output
- US-002 → Accurate answer generation
- US-003 → Source citation
- US-004 → Expense rule enforcement
- US-006 → Holiday logic
- US-007 → Security filtering
- US-009 → API endpoint
- US-010 → Document ingestion
- US-011 → Retrieval system

---

## 10. Estimation (Optional)

| Story ID | Complexity | Notes           |
| -------- | ---------- | --------------- |
| US-001   | S          | UI basic        |
| US-002   | M          | LLM + retrieval |
| US-003   | M          | citation logic  |
| US-004   | S          | rule-based      |
| US-006   | M          | logic + data    |
| US-007   | M          | filtering       |
| US-009   | S          | API setup       |
| US-010   | M          | ingestion       |
| US-011   | M          | retrieval       |

---

## 11. Definition of Ready Check

All Sprint 1 stories:

- Clearly defined
- Acceptance criteria written
- Technically feasible
- Prioritized

---

## 12. Decision Statement

This backlog represents a **focused MVP scope**, prioritizing:

- Accuracy
- Security
- Policy enforcement
- Source transparency

All future development must build on this foundation.

---
