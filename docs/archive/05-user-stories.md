# User Stories Backlog

> Archive note: This is a historical story set. It has been updated into a more Scrum-friendly format, but the active planning source is still `backlog.md`.

## GreenLeaf Logistics - Beat-Bot

## 1. Story Writing Rules

This archive version follows a simpler Scrum-style structure:

- one clear user or system goal per story
- explicit business value
- testable acceptance criteria
- no hidden implementation detail inside the story sentence

## 2. Roles

- `Employee`
- `Admin`
- `Developer`
- `System`

## 3. MVP User Stories

### US-001 - Ask a Policy Question

**Story**  
As an `Employee`, I want to ask a policy question in natural language so that I can get help quickly.

**Acceptance Criteria**

- The user can submit a text question
- The system returns a response in the chat UI
- Empty or invalid requests are handled safely

### US-002 - Receive a Source-Backed Answer

**Story**  
As an `Employee`, I want answers to be grounded in approved sources so that I can trust the assistant.

**Acceptance Criteria**

- Answers are based only on approved sources
- Unsupported answers are refused or downgraded safely
- The system does not invent policy details

### US-003 - See the Source

**Story**  
As an `Employee`, I want to see the source of an answer so that I can verify it myself.

**Acceptance Criteria**

- Responses include a human-readable citation
- Citation points to the supporting document and section
- Page number is shown when available

### US-004 - Enforce the Expense Limit

**Story**  
As the `System`, I want to reject expense requests above 35 CHF per person so that company policy is enforced correctly.

**Acceptance Criteria**

- Expense values above 35 CHF per person are rejected
- The response explains the reason clearly
- The result remains traceable in logs or audit metadata

### US-005 - Reject Alcohol Expenses

**Story**  
As the `System`, I want to reject alcohol-related expense requests so that reimbursement policy is enforced correctly.

**Acceptance Criteria**

- Alcohol-related expense requests are rejected
- The response explains the reason clearly
- The result remains traceable in logs or audit metadata

### US-006 - Answer Basel Holiday Questions Correctly

**Story**  
As an `Employee`, I want correct holiday answers for Basel-Stadt so that I can plan my work accurately.

**Acceptance Criteria**

- May 1 is handled correctly for Basel-Stadt
- National and cantonal holiday cases are distinguished correctly
- The response can cite the supporting source

### US-007 - Refuse Sensitive IT Questions

**Story**  
As the `System`, I want to refuse sensitive IT questions so that restricted information is protected.

**Acceptance Criteria**

- Internal Wi-Fi password requests are refused
- Guest Wi-Fi password requests are refused in the MVP
- MAC registration detail requests are refused
- Safe redirection to IT is possible

### US-008 - Redirect Misconduct Topics

**Story**  
As an `Employee`, I want misconduct-related questions redirected safely so that I use the correct process.

**Acceptance Criteria**

- Harassment and bullying are not handled as standard Q&A
- Whistleblowing is redirected to the ombudsman path
- The response language is safe and clear

### US-009 - Expose an Ask API

**Story**  
As a `Developer`, I want a working `/ask` endpoint so that the frontend can communicate with the backend.

**Acceptance Criteria**

- The endpoint exists
- Request and response schemas are defined
- Invalid input is handled safely

### US-010 - Generate a Structured Draft

**Story**  
As the `System`, I want the model to return a structured draft so that backend validators can inspect it safely before release.

**Acceptance Criteria**

- Draft includes answer text
- Draft includes response type
- Draft includes citations when applicable
- Draft is not released before validation

### US-011 - Ingest Approved Sources

**Story**  
As the `System`, I want approved documents ingested into a searchable store so that the assistant can retrieve evidence.

**Acceptance Criteria**

- Handbook content is parsed, chunked, and stored
- Holiday CSV is loaded
- Metadata is available for retrieval and citation

### US-012 - Retrieve Relevant Evidence

**Story**  
As the `System`, I want to retrieve relevant content before answering so that the answer is grounded.

**Acceptance Criteria**

- Retrieval returns relevant chunks
- Irrelevant content is limited
- Retrieved context can be cited

### US-013 - Validate Generated Drafts

**Story**  
As the `System`, I want post-generation validators so that unsafe, inconsistent, or uncited drafts are blocked.

**Acceptance Criteria**

- Schema validation exists
- Citation validation exists
- Disclosure validation exists
- High-risk consistency checks exist
- Failed drafts do not reach the user directly

### US-014 - Review Chat History as Admin

**Story**  
As an `Admin`, I want to review employee chat history so that I can investigate system behavior.

**Acceptance Criteria**

- Admin can view all employee chat histories and related metadata
- Employees can view only their own history
- Chat history is persisted in the application database

## 4. Lower-Priority Stories

### US-015 - Readable Answer Formatting

**Story**  
As an `Employee`, I want clear answer formatting so that the response is easy to scan.

### US-016 - Consistent System Behavior

**Story**  
As an `Admin`, I want consistent answers so that employees receive reliable guidance.

### US-017 - Review Logs for Debugging

**Story**  
As a `Developer`, I want logs for requests, validator outcomes, and responses so that I can debug and evaluate behavior.

## 5. Out of Scope Stories

- salary increase workflows
- payroll discussions
- HR case management
- logistics tracking
- self-service disclosure of sensitive technical access details
