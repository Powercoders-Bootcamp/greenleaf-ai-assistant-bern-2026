# User Stories Backlog

## GreenLeaf Logistics - Beat-Bot

## 1. Core Roles

- Employee
- Admin
- System

## 2. MVP User Stories

### US-001

As an Employee, I want to ask a policy question in natural language so that I can get an answer quickly.

**Acceptance Criteria**

- User can submit a text question
- The system returns a structured response
- The response is visible in the UI

### US-002

As an Employee, I want trusted answers from the handbook so that I can rely on the assistant.

**Acceptance Criteria**

- Answers are grounded in approved sources only
- The system refuses when it cannot answer safely
- The system does not invent policy details

### US-003

As an Employee, I want to see the source of an answer so that I can verify it myself.

**Acceptance Criteria**

- Responses include a human-readable citation
- Citation points to the supporting section or document

### US-004

As the System, I must reject expenses above 35 CHF per person so that company policy is enforced.

**Acceptance Criteria**

- Expense values above 35 CHF are rejected
- The response explains the rule

### US-005

As the System, I must reject alcohol expenses so that company policy is enforced.

**Acceptance Criteria**

- Alcohol-related expense requests are rejected
- The response explains the rule

### US-006

As an Employee, I want correct holiday answers for Basel-Stadt so that I can plan my work.

**Acceptance Criteria**

- May 1 is treated correctly for Basel-Stadt
- National and cantonal holidays are handled correctly

### US-007

As the System, I must refuse sensitive IT questions so that restricted information is protected.

**Acceptance Criteria**

- Internal Wi-Fi password requests are refused
- Guest Wi-Fi password requests are refused in the MVP
- MAC registration detail requests are refused
- Safe redirection to IT is available

### US-008

As an Employee, I want misconduct-related questions redirected safely so that I use the correct process.

**Acceptance Criteria**

- Harassment and bullying are not handled as standard Q&A
- Whistleblowing is redirected to the ombudsman path

### US-009

As a Developer, I want a working `/ask` endpoint so that the frontend can communicate with the backend.

**Acceptance Criteria**

- Endpoint exists
- Request and response schemas are defined
- Invalid input is handled safely

### US-010

As the System, I want approved documents ingested into a searchable store so that the assistant can retrieve evidence.

**Acceptance Criteria**

- Handbook content is chunked and stored
- Holiday CSV is loaded
- Metadata is available for retrieval and citation

### US-011

As the System, I must retrieve relevant content before answering so that the answer is grounded.

**Acceptance Criteria**

- Retrieval returns relevant chunks
- Irrelevant content is limited
- Retrieved context can be cited

## 3. Lower-Priority Stories

### US-012

As an Employee, I want clear answer formatting so that the response is easy to scan.

### US-013

As an Admin, I want consistent answers so that employees receive reliable guidance.

### US-014

As a Developer, I want logs for questions and responses so that I can debug and evaluate behavior.

### US-015

As an Admin, I want basic visibility into system behavior so that I can review reliability.

## 4. Out of Scope Stories

- salary increase workflows
- payroll discussions
- HR case management
- logistics tracking
- self-service disclosure of sensitive technical access details
