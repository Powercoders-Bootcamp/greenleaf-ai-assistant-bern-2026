# Requirements Specification

## GreenLeaf Logistics - Beat-Bot

## 1. Purpose

This document defines the functional and non-functional requirements for Beat-Bot based on the handbook, the stakeholder briefing, and the holiday CSV.

## 2. Functional Requirements

### 2.1 Question Handling

- The system shall accept natural-language questions from users
- The system shall require authenticated user login before question access is granted
- The system shall support single-turn interactions and limited clarification turns
- The system shall validate incoming requests before processing

### 2.1.0 Identity and Roles

- The system shall support exactly two MVP roles: `Employee` and `Admin`
- The system shall store user-role mapping in the application database
- The system shall allow each `Employee` to view only their own conversation history
- The system shall allow `Admin` users to view all employee conversation histories and related metadata
- The system shall use identity-based access for MVP without requiring managed-device checks

### 2.1.1 LLM Draft Generation

- The system shall use the LLM as the primary interpretation layer for user questions
- The LLM shall return a structured draft response rather than only free text
- The structured draft should include fields such as:
  - `answer_text`
  - `response_type`
  - `citations`
  - `decision`
  - `needs_clarification`
  - `sensitive_topic`

### 2.1.2 AI-Assisted Helper Tasks

- The system may use the same AI layer for translation or normalization
- The system may use the same AI layer for future speech-to-text transcription
- Helper AI behavior shall still be subject to backend validation before release

### 2.1.3 Post-Generation Validation

- The system shall validate every structured draft before returning it to the user
- Validation shall include:
  - schema validation
  - citation validation
  - disclosure validation
  - consistency validation for high-risk policy areas
  - response-type validation for redirect/refusal scenarios
- If validation fails, the system shall retry with a stricter instruction or return a safe fallback

### 2.2 Source-Limited Answering

- The system shall answer only from approved internal sources
- The system shall refuse when sufficient evidence is not available
- The system shall not invent policy details or citations

### 2.3 Source Referencing

- The system shall include source references in trusted responses
- The system shall identify the document and section used
- The system should include page number when available
- The system shall validate citations before returning the answer

### 2.4 Expense Policy Enforcement

- The system shall reject expense requests above 35 CHF per person
- The system shall reject expense requests involving alcohol
- The system shall explain the relevant policy rule in the response
- The system shall use structured fact extraction for expense validation instead of relying only on raw string matching
- The system shall request clarification when expense-critical fields are missing, such as amount, person count, alcohol status, or external client presence

### 2.5 Holiday Policy Enforcement

- The system shall answer Swiss national holidays correctly
- The system shall apply Basel-Stadt-specific handling for Labor Day on May 1
- The system shall distinguish national and cantonal holiday rules

### 2.6 Sensitive Topic Handling

- The system shall refuse to disclose internal Wi-Fi credentials
- The system shall refuse to disclose guest Wi-Fi passwords in the MVP
- The system shall refuse to disclose MAC address registration details
- The system shall redirect users to IT when safe process guidance is appropriate

### 2.7 Misconduct Redirection

- The system shall not handle harassment, bullying, or whistleblowing as normal Q&A
- The system shall redirect those cases to the approved ombudsman process

### 2.8 Data Ingestion

- The system shall ingest the handbook into a searchable structure
- The system shall ingest the 2026 holiday CSV for deterministic use
- The system shall preserve metadata needed for citations and filtering

### 2.9 Logging and Traceability

- The system shall log query handling steps needed for debugging and evaluation
- The system shall make validation outcomes and retrieved sources traceable
- The system shall persist conversation history and related metadata
- The system shall enforce role-based access to conversation history

## 3. Non-Functional Requirements

### 3.1 Accuracy

- The system must prioritize correctness over completeness
- The system must avoid hallucinations
- The system must behave reliably on critical business scenarios

### 3.2 Security

- The system must prevent disclosure of restricted technical access information
- The system must fail safely when policy or evidence is unclear
- The system must not expose secrets in code or logs
- The system must not disclose Wi-Fi passwords or MAC registration details even when such topics are mentioned in source content
- The system must keep identity, role, and authorization logic in the backend rather than delegating those decisions to the LLM
- The system must not expose full user data or full chat history to the LLM by default

### 3.3 Reliability

- The system must behave consistently for equivalent inputs
- The system must handle unsupported requests safely
- The system must not release a draft that fails a critical validator

### 3.4 Performance

- The MVP should return responses within an acceptable user-facing time
- The system should remain responsive for basic internal usage

### 3.5 Auditability

- Every trusted answer must be traceable to supporting evidence
- Critical decisions and refusals must be inspectable

## 4. Product Interpretation Notes

- Presence of a fact in a source document does not automatically mean the bot may disclose it to every user
- Stakeholder security expectations override broad source recall for sensitive IT-access topics
- Lightweight validators should prefer structured facts over brittle substring blocking when checking policy consistency or disclosure risk
- The LLM should receive only the minimum necessary request context selected by the backend

## 5. Acceptance Criteria at Product Level

The system is acceptable if it:

- rejects invalid expense scenarios
- answers Basel holiday questions correctly
- returns source-backed answers for supported policy questions
- refuses sensitive access questions safely
- redirects misconduct questions correctly
