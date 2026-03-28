# Sprint 1 Plan

## GreenLeaf Logistics – Beat-Bot

---

## 1. Sprint Overview

**Sprint Duration:** Week 1 – Week 2  
**Sprint Goal:**  
Deliver a functional MVP foundation that can:

- Accept user questions
- Retrieve relevant handbook information
- Generate source-backed responses
- Enforce basic policy rules
- Safely handle restricted or uncertain queries

---

## 2. Sprint Objectives

By the end of Sprint 1, the team should have:

- A working chat interface (basic)
- A functional backend API (`/ask`)
- Handbook ingestion pipeline
- Retrieval system (basic)
- Rule-based policy enforcement (expenses)
- Source citation in responses
- Basic refusal and fallback logic

---

## 3. Sprint Scope (Selected User Stories)

Included:

- US-001 → Question input/output
- US-002 → Accurate answer generation
- US-003 → Source citation
- US-004 → Expense rule enforcement
- US-006 → Holiday logic (basic)
- US-007 → Security filtering (basic)
- US-009 → API endpoint
- US-010 → Document ingestion
- US-011 → Retrieval system

---

## 4. Sprint Backlog (Tasks Breakdown)

---

### US-001: Question Input & Output (Frontend)

**Tasks:**

- Create basic chat UI (input field + message display)
- Handle user input submission
- Display responses from API
- Handle loading and error states

**Owner:** Frontend Dev  
**Estimate:** Small

---

### US-002: Answer Generation (Backend + AI)

**Tasks:**

- Integrate LLM API
- Design prompt structure
- Implement structured response format
- Handle fallback for low confidence

**Owner:** Backend Dev  
**Estimate:** Medium

---

### US-003: Source Citation

**Tasks:**

- Attach source metadata to retrieved chunks
- Include source in response payload
- Display source in UI

**Owner:** Backend + Frontend  
**Estimate:** Medium

---

### US-004: Expense Rule Enforcement

**Tasks:**

- Implement rule:
  - > 35 CHF → reject
  - alcohol → reject
- Add rule-check logic before LLM call
- Return deterministic response

**Owner:** Backend Dev  
**Estimate:** Small

---

### US-006: Holiday Logic

**Tasks:**

- Implement basic holiday dataset
- Handle Basel-specific logic
- Return correct holiday status

**Owner:** Backend Dev  
**Estimate:** Medium

---

### US-007: Security Filtering

**Tasks:**

- Define sensitive keywords/topics
- Implement basic query filtering
- Add refusal response for restricted queries

**Owner:** Backend Dev  
**Estimate:** Medium

---

### US-009: API Endpoint

**Tasks:**

- Create `/ask` endpoint
- Define request/response schema
- Handle input validation
- Return structured response

**Owner:** Backend Dev  
**Estimate:** Small

---

### US-010: Document Ingestion

**Tasks:**

- Parse handbook PDF
- Split into chunks (section-based)
- Add metadata (page, section)
- Generate embeddings
- Store in database

**Owner:** Backend Dev  
**Estimate:** Medium

---

### US-011: Retrieval System

**Tasks:**

- Implement vector search (pgvector)
- Add metadata filtering
- Return top relevant chunks
- Integrate with answer generation

**Owner:** Backend Dev  
**Estimate:** Medium

---

## 5. Task Ownership Summary

| Area        | Responsible Role |
| ----------- | ---------------- |
| Frontend    | Frontend Dev     |
| Backend API | Backend Dev      |
| AI / LLM    | Backend Dev      |
| Retrieval   | Backend Dev      |
| Rules       | Backend Dev      |
| QA          | QA Engineer      |

---

## 6. Timeline (Suggested)

### Week 1

- Setup repo, environment, base structure
- Implement ingestion pipeline
- Setup database
- Build basic API endpoint
- Start frontend UI

---

### Week 2

- Implement retrieval
- Integrate LLM
- Add rule-based logic
- Add source citation
- Add security filtering
- End-to-end testing

---

## 7. Dependencies

- Handbook PDF availability
- LLM API access
- Database setup (PostgreSQL + pgvector)
- Development environment ready

---

## 8. Risks in Sprint 1

- Retrieval not accurate enough
- LLM output not controllable
- Time underestimated for ingestion
- Over-focus on UI instead of core logic

---

## 9. Mitigation Strategy

- Start with simple pipeline
- Focus on core logic first (backend)
- Use small test dataset
- Validate with golden questions early

---

## 10. Definition of Success (Sprint 1)

Sprint 1 is successful if:

- A user can ask a question end-to-end
- The system returns a grounded answer
- Source is shown
- Expense rule is enforced correctly
- Unsafe queries are handled safely

---

## 11. Demo Scenario (End of Sprint)

Demonstrate:

1. Ask: “Can I expense a 36 CHF lunch?”  
   → System rejects correctly

2. Ask: “Is May 1st a holiday in Basel?”  
   → Correct answer

3. Ask: “What is the Wi-Fi password?”  
   → Refusal or safe response

4. Ask: “How many vacation days do I have?”  
   → Source-backed answer

---

## 12. Decision Statement

Sprint 1 focuses on delivering a **functional, safe, and reliable MVP core**, prioritizing:

- Accuracy over completeness
- Safety over flexibility
- Core functionality over UI polish

All non-essential features are deferred.

---
