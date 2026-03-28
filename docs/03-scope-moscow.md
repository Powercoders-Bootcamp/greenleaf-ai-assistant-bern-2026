# Stakeholder Analysis & MoSCoW Prioritization

## GreenLeaf Logistics – Beat-Bot

---

## 1. Stakeholder Overview

The Beat-Bot project involves multiple stakeholders with different expectations, levels of influence, and areas of concern. Understanding these stakeholders is critical to defining product scope, priorities, and success criteria.

---

## 2. Key Stakeholders

### 2.1 Employees (Primary Users)

**Role:** End users of the system  
**Description:**  
Employees across departments (warehouse, office, support) who need quick and reliable answers to company policies.

**Needs:**

- Fast and accurate answers
- Simple and intuitive interaction
- Clear explanations of policies
- Trustworthy and consistent responses

**Pain Points:**

- Difficulty finding information in the handbook
- Repetitive manual clarification from Admin
- Uncertainty about policies (expenses, holidays, leave)

---

### 2.2 Admin (Operations / Product Owner Perspective)

**Role:** Primary stakeholder and decision-maker  
**Description:**  
Represents operational leadership responsible for enforcing company rules and reducing repetitive workload.

**Needs:**

- Reduction of repetitive employee questions
- Strict enforcement of company policies
- High accuracy and reliability
- Control over system behavior

**Critical Expectations:**

- No guessing on financial matters
- Basel-Stadt specific holiday accuracy
- No leakage of sensitive information
- Ability to reference exact source of answers

---

### 2.3 IT & Security

**Role:** Security and compliance authority  
**Description:**  
Responsible for ensuring that company systems do not expose sensitive or restricted information.

**Needs:**

- Secure handling of data
- Controlled access to sensitive information
- Prevention of credential leakage
- Compliance with internal security standards

**Concerns:**

- Unauthorized access to internal data
- Exposure of credentials or system details
- Misuse of AI-generated responses

---

### 2.4 Project Team

**Role:** Delivery and implementation  
**Description:**  
Responsible for designing, building, and delivering the solution.

**Needs:**

- Clear requirements and scope
- Defined priorities
- Manageable workload within sprint cycles
- Alignment with stakeholder expectations

---

## 3. Stakeholder Influence vs Interest

| Stakeholder   | Influence | Interest | Priority Level |
| ------------- | --------- | -------- | -------------- |
| Admin         | High      | High     | Critical       |
| Employees     | Medium    | High     | High           |
| IT & Security | High      | Medium   | High           |
| Project Team  | Medium    | High     | High           |

---

## 4. MoSCoW Prioritization

The MoSCoW method is used to define feature priority:

- **Must Have** → Critical for MVP success
- **Should Have** → Important but not blocking
- **Could Have** → Nice-to-have enhancements
- **Won’t Have** → Explicitly out of scope

---

## 5. Must Have (Critical Features)

These features are mandatory for the system to be usable and accepted.

### Core Functionality

- Answer employee questions based on handbook content
- Provide accurate and consistent responses
- Include source references for each answer

### Policy Enforcement

- Enforce expense rules:
  - Maximum 35 CHF per person
  - No alcohol reimbursement
- Correct handling of holiday logic (Basel-Stadt specific)

### Security

- Prevent disclosure of sensitive information
- Block unsafe or restricted queries
- Implement basic access control

### Reliability

- Avoid hallucinations (no guessing)
- Only answer when sufficient information is available
- Provide safe fallback or refusal when uncertain

---

## 6. Should Have (Important Features)

These features improve usability and trust but are not strictly required for MVP.

- Natural language interaction
- Clear and concise answer formatting
- Highlighted source references
- Basic role-based access control
- Structured responses (answer + source + confidence)
- Logging of queries and responses

---

## 7. Could Have (Optional Enhancements)

These features enhance the product but are not required in early stages.

- Friendly conversational tone
- Slack or external integrations
- Admin dashboard for monitoring usage
- Analytics on common questions
- Suggested follow-up questions
- Multi-language support

---

## 8. Won’t Have (Out of Scope)

The following features are explicitly excluded from the project scope:

- Salary increase processing
- Compensation or payroll discussions
- Logistics tracking or warehouse operations
- Handling of misconduct or HR complaints
- Access to confidential credentials or internal technical details
- Full enterprise system integrations
- Real-time data synchronization with external systems

---

## 9. Scope Boundaries

### Included

- Internal AI assistant
- Handbook-based knowledge system
- Question-answer functionality
- Source-backed responses
- Basic UI and backend system
- Initial security filtering

### Excluded

- Full HR system automation
- Operational system integration
- Complex workflow automation
- Advanced reporting tools

---

## 10. Key Risks Identified

### Technical Risk

- Retrieval may fail to provide relevant context for accurate answers

### Product Risk

- Incorrect answers may reduce trust in the system

### Security Risk

- Potential exposure of sensitive information if not properly filtered

### Team Risk

- Misalignment on priorities or scope creep

---

## 11. Risk Mitigation Strategy

- Implement strict policy-based validation rules
- Use controlled retrieval and source verification
- Apply security filters and refusal mechanisms
- Maintain a clearly prioritized backlog
- Validate system with real test scenarios

---

## 12. Key Takeaways

- Accuracy, security, and trust are the highest priorities
- The system must behave deterministically for critical rules
- Scope discipline is essential for MVP success
- Not all features are needed in the first version

---

## 13. Decision Statement

The Beat-Bot MVP will focus on **policy-accurate, source-backed question answering** with strict enforcement of business rules and security constraints.

All additional features will be considered only after core reliability is proven.

---
