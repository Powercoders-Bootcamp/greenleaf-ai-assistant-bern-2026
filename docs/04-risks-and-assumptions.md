# Project Boundary Map & Scope Definition

## GreenLeaf Logistics – Beat-Bot

---

## 1. Purpose of This Document

This document defines the **explicit boundaries of the Beat-Bot system**, including:

- What the system **will do**
- What the system **will NOT do**
- Where responsibility lies between the system and humans
- Key risks and constraints

The goal is to prevent scope creep and ensure alignment between product, technical implementation, and stakeholder expectations.

---

## 2. System Vision (Reinforced)

Beat-Bot is a **policy-aware internal AI assistant** designed to:

- Answer employee questions based on approved internal documents
- Provide **accurate, deterministic, and source-backed responses**
- Reduce operational interruptions for Admin users
- Maintain strict **security and compliance boundaries**

---

## 3. Core System Capabilities

### 3.1 Question Answering

- Accept natural language questions from employees
- Retrieve relevant information from internal sources
- Generate clear and concise responses

---

### 3.2 Source Referencing

- Provide traceable references to handbook sections
- Enable users to verify answers independently

---

### 3.3 Policy Enforcement

- Apply deterministic business rules (e.g., expense limits)
- Reject invalid or non-compliant requests

---

### 3.4 Security Filtering

- Detect sensitive or restricted topics
- Prevent unauthorized disclosure of information
- Provide safe fallback or refusal responses

---

### 3.5 Controlled AI Behavior

- Avoid hallucinations
- Only answer based on verified sources
- Refuse to answer when confidence is low

---

## 4. System Boundaries

### 4.1 In-Scope Functional Boundaries

The system WILL:

- Answer handbook-related questions
- Provide policy explanations
- Enforce clearly defined rules
- Show source references
- Handle structured and unstructured queries
- Log interactions for evaluation

---

### 4.2 Out-of-Scope Functional Boundaries

The system WILL NOT:

- Process salary changes or compensation decisions
- Handle HR case management (e.g., harassment, disputes)
- Provide legal or compliance advice
- Perform operational logistics tasks
- Access or expose confidential credentials
- Replace human decision-making in complex cases

---

## 5. Responsibility Split

### 5.1 System Responsibilities

- Provide accurate, policy-based answers
- Enforce business rules deterministically
- Protect sensitive information
- Provide transparent sources
- Refuse unsafe or unknown queries

---

### 5.2 Human Responsibilities

- Interpret complex or ambiguous cases
- Approve exceptional requests
- Handle sensitive HR or misconduct issues
- Maintain and update policy documents
- Review and validate system outputs (when needed)

---

## 6. AI Responsibility Boundaries

The AI assistant:

### CAN:

- Answer factual questions from approved sources
- Explain policies
- Provide guidance within defined rules

### CANNOT:

- Make discretionary decisions
- Interpret ambiguous real-world situations beyond policy
- Access external or real-time systems
- Override company policies
- Generate answers without source support

---

## 7. Data Boundaries

### Allowed Data Sources

- Employee handbook
- Approved internal policy documents
- Structured business rules (e.g., expense limits)

---

### Restricted Data

- Internal credentials (passwords, MAC addresses)
- Sensitive HR data
- Personal employee information
- Confidential system configurations

---

## 8. Interaction Boundaries

### Supported Interaction

- Text-based question-answer interaction
- Single-turn and simple multi-turn queries

---

### Not Supported (MVP)

- Complex multi-step workflows
- Voice interaction
- External system actions
- Autonomous decision-making

---

## 9. Key Constraints

- Limited project timeline (Weeks 1–4)
- High accuracy requirements
- Strict security expectations
- Limited initial data sources
- MVP-first approach (no over-engineering)

---

## 10. Risk Analysis

### 10.1 Technical Risks

**Risk:** Poor retrieval quality leads to incorrect answers  
**Impact:** Loss of trust, system rejection  
**Mitigation:**

- Hybrid retrieval approach
- Evaluation with test questions
- Iterative tuning

---

### 10.2 AI/Model Risks

**Risk:** Hallucinated or unsupported answers  
**Impact:** Incorrect information provided to employees  
**Mitigation:**

- Source-only answering policy
- Refusal mechanism
- Structured outputs

---

### 10.3 Security Risks

**Risk:** Exposure of sensitive information  
**Impact:** Security breach and stakeholder rejection  
**Mitigation:**

- Query filtering
- Role-based access control
- Sensitive topic detection

---

### 10.4 Product Risks

**Risk:** Misalignment with stakeholder expectations  
**Impact:** Low adoption or project failure  
**Mitigation:**

- Clear prioritization (MoSCoW)
- Regular stakeholder validation
- Focus on critical use cases

---

### 10.5 Team Risks

**Risk:** Over-engineering or scope creep  
**Impact:** Delayed delivery or incomplete MVP  
**Mitigation:**

- Strict scope boundaries
- Sprint discipline
- MVP-first mindset

---

## 11. Boundary Scenarios (Examples)

### Scenario 1: Expense Question

User asks: “Can I expense a 36 CHF lunch?”  
→ System MUST reject (rule-based)

---

### Scenario 2: Holiday Question

User asks: “Is May 1st a holiday in Basel?”  
→ System MUST answer correctly using Basel-specific logic

---

### Scenario 3: Sensitive IT Question

User asks: “What is the internal Wi-Fi setup?”  
→ System MUST refuse or limit response

---

### Scenario 4: Misconduct Question

User asks: “How do I report harassment?”  
→ System MUST redirect to proper channel (not answer directly)

---

## 12. Boundary Enforcement Principles

- When in doubt → **do not answer**
- When sensitive → **restrict or redirect**
- When rule-based → **enforce deterministically**
- When answering → **always provide source**

---

## 13. Decision Statement

The Beat-Bot system will operate within **strict functional, data, and behavioral boundaries** to ensure accuracy, security, and trust.

The system is not a general-purpose chatbot, but a **controlled policy assistant with clearly defined limits**.

---
