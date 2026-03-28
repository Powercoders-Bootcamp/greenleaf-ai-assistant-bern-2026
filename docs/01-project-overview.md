# Project Charter

## GreenLeaf Logistics – Beat-Bot

## 1. Project Overview

**Project Name:** Beat-Bot  
**Company:** GreenLeaf Logistics  
**Business Sponsor:** GreenLeaf Logistics Operations Management  
**Primary Stakeholder Role:** Admin / Head of Operations  
**Project Type:** Internal AI Assistant / Policy Q&A System  
**Project Duration:** Weeks 1–4 (initial project phase)

The purpose of this project is to design and deliver an internal AI assistant that helps automate repetitive employee questions by using approved company policy sources, primarily the GreenLeaf Logistics handbook and related official business rules.

The assistant must reduce repetitive interruptions for operations management while ensuring that responses remain accurate, secure, and traceable to authoritative sources. The stakeholder has made clear that the system must not hallucinate, must not guess on policy-sensitive questions, and must be able to show the exact source of each answer. :contentReference[oaicite:2]{index=2}

---

## 2. Business Problem

GreenLeaf Logistics currently faces repeated operational interruptions caused by employees asking the same policy and handbook-related questions. These recurring questions reduce management efficiency and create unnecessary dependency on manual responses from operations leadership. :contentReference[oaicite:3]{index=3}

Examples of recurring questions include:

- Public holiday eligibility
- Expense reimbursement rules
- Leave and attendance questions
- Policy interpretation requests

The current problem is not a lack of written policy, but a lack of accessible, trusted, and consistently applied answers.

---

## 3. Project Goal

The goal of the project is to deliver a reliable internal AI assistant that:

- Answers repetitive employee questions based on approved company sources
- Provides accurate and policy-aligned answers
- Includes source references for trust and traceability
- Prevents unsafe or unauthorized disclosures
- Reduces operational overhead for Admin and management users

---

## 4. Project Objectives

### Primary Objectives

- Provide fast and accurate answers to common employee handbook questions
- Reduce manual interruptions for operations leadership
- Ensure all answers are grounded in approved internal sources
- Enforce strict policy behavior on sensitive topics such as expenses and security

### Secondary Objectives

- Establish a maintainable technical foundation for future iterations
- Create a transparent and auditable answer flow
- Build an MVP that can be validated during the first project phase

---

## 5. Success Criteria

The project will be considered successful if the MVP can demonstrate the following:

- The assistant answers handbook-related questions accurately
- The assistant provides source-backed responses
- The assistant correctly applies hard rules for expense validation
- The assistant correctly handles Basel-Stadt holiday logic
- The assistant refuses or safely redirects unsafe or sensitive requests
- The team has a clearly defined process, backlog, and sprint plan in place

These success criteria directly reflect the stakeholder’s stated non-negotiables: no guessing on money, Basel-specific holiday accuracy, security-first operation, and proof of source. :contentReference[oaicite:4]{index=4}

---

## 6. In-Scope

The following items are included in the initial project scope:

- Internal AI assistant for employee policy questions
- Handbook-based question answering
- Source citation in responses
- Basic authentication and role-aware access model
- Expense-policy validation support
- Holiday and leave-policy support
- Initial security filtering for restricted topics
- MVP user interface
- Sprint-based Agile delivery setup
- GitHub-based project tracking and backlog management

---

## 7. Out of Scope

The following items are explicitly out of scope for the first project phase:

- Salary increase processing
- Compensation negotiations
- Physical mail handling
- Logistics tracking or warehouse operations data
- Full HR case management
- Whistleblowing or misconduct case handling through the bot
- Open access to confidential credentials or internal technical identifiers
- Advanced analytics dashboard
- Real-time integrations with external enterprise systems

This boundary is supported by the handbook’s instruction that serious misconduct, harassment, bullying, and whistleblowing matters must not be handled via the internal bot and should instead be directed to the external ombudsman. :contentReference[oaicite:5]{index=5}

---

## 8. Key Assumptions

The project is based on the following assumptions:

- The employee handbook is the initial primary source of truth
- Early users will mainly ask repetitive operational and policy questions
- Most MVP use cases can be answered from a limited set of approved internal documents
- The first version does not need to support all possible business processes
- The team can deliver a functional MVP within the project timeline if scope is kept disciplined

---

## 9. Known Constraints

- Short initial delivery window
- Limited implementation time before sprint execution
- Need for high trust despite early-stage product maturity
- Strict stakeholder tolerance for incorrect answers
- Sensitive content areas that require refusal or escalation behavior

---

## 10. Major Risks

### Technical Risk

The retrieval pipeline may return incomplete or weak context, causing inaccurate answers or weak source grounding.

### Product Risk

The assistant may be perceived as untrustworthy if it fails on critical examples such as holiday logic, expense thresholds, or citation quality.

### Team Risk

The team may spend too much time building general chatbot functionality instead of focusing on policy-critical workflows.

---

## 11. Key Stakeholders

- **Employees** – primary end users asking policy-related questions
- **Admin** – operational owner and decision-maker expecting reliable automation
- **IT / Security** – responsible for ensuring secure information handling
- **Project Team** – responsible for delivery, quality, and Agile execution

---

## 12. Product Principles

The Beat-Bot must be built according to the following principles:

- **Accuracy over creativity**
- **Source-backed answers only**
- **Security by default**
- **Policy-first logic**
- **Simple MVP before advanced features**
- **Clear escalation for sensitive matters**

---

## 13. Initial Deliverables

By the middle of Week 2, the team should have prepared:

- Team Charter
- Project requirements and scoped backlog
- GitHub Kanban board with user stories
- Communication plan in the project wiki
- Stakeholder analysis and MoSCoW prioritization
- Scope and boundary definition
- Initial risk identification
- Definition of Done
- Sprint 1 readiness materials

---

## 14. Project Approval Statement

This charter defines the initial business intent, scope direction, and success conditions for the Beat-Bot project. It establishes the foundation for Agile planning, requirements refinement, architectural design, and sprint execution.

The project may proceed to the next stage: **Team Charter and Stakeholder Analysis**.
