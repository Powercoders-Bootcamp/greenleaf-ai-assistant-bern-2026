# Definition of Ready (DoR) & Definition of Done (DoD)

## GreenLeaf Logistics – Beat-Bot

---

## 1. Purpose

This document defines the criteria for:

- When a user story is **ready to be worked on** (DoR)
- When a user story is considered **fully complete** (DoD)

It ensures:

- Clarity before development
- Quality and consistency after implementation
- Alignment across Product, Engineering, and QA

---

## 2. Definition of Ready (DoR)

A user story is considered **Ready** when all the following criteria are met:

### 2.1 Clarity

- The user story follows the format:
  - As a [role], I want [goal], so that [benefit]
- The purpose of the story is clearly understood
- The expected outcome is well defined

---

### 2.2 Acceptance Criteria

- Acceptance criteria are clearly written
- Criteria are testable and measurable
- Edge cases are identified where applicable

---

### 2.3 Scope & Boundaries

- The scope of the story is clearly defined
- Out-of-scope elements are identified if needed
- Dependencies are known

---

### 2.4 Technical Readiness

- Required technical approach is understood
- No major unknowns or blockers remain
- Required data sources are available

---

### 2.5 Estimation

- The story has been estimated (e.g., story points or size)
- The team agrees on complexity

---

### 2.6 Prioritization

- The story is prioritized in the backlog
- It aligns with sprint goals

---

### 2.7 Team Alignment

- The team has discussed the story
- Questions have been clarified
- All roles (PO, Dev, QA) understand the requirements

---

## 3. Definition of Done (DoD)

A user story is considered **Done** only when all the following criteria are met:

---

### 3.1 Functional Completion

- The feature is fully implemented
- All acceptance criteria are satisfied
- The system behaves as expected

---

### 3.2 Code Quality

- Code is clean, readable, and maintainable
- Code follows agreed standards
- Code has been peer-reviewed and approved

---

### 3.3 Testing

- Feature has been tested (manual or automated)
- Edge cases are validated
- No critical bugs remain

---

### 3.4 AI-Specific Quality (Critical for this project)

- Responses are:
  - accurate
  - grounded in source content
  - free of hallucinations
- Deterministic rules (e.g., expense limits) are correctly enforced
- Refusal logic works correctly for unsafe queries
- Sensitive information is not exposed

---

### 3.5 Source Validation

- All answers include valid source references
- Sources match retrieved content
- No fabricated citations are present

---

### 3.6 Security Compliance

- No sensitive data is exposed
- Access control rules are respected
- Input validation is implemented

---

### 3.7 Performance (MVP Level)

- Response time is within acceptable limits
- No major performance issues observed

---

### 3.8 Logging & Observability

- Relevant logs are generated
- Errors are properly handled
- Outputs are traceable for debugging

---

### 3.9 Documentation

- Relevant documentation is updated
- Changes are reflected in system documentation if needed

---

### 3.10 Deployment Readiness

- Feature is deployable
- No blocking issues remain
- Ready for demonstration or release

---

## 4. DoD Checklist (Quick Reference)

A story is Done if:

- [ ] Acceptance criteria met
- [ ] Code reviewed
- [ ] Tested and validated
- [ ] No critical bugs
- [ ] Accurate and safe responses
- [ ] Source references correct
- [ ] Security checks passed
- [ ] Logs available
- [ ] Documentation updated

---

## 5. Special Rules for AI Features

For any AI-related functionality:

- The system must **not guess**
- The system must **only answer based on verified sources**
- The system must **refuse unsafe or unsupported queries**
- The system must **apply deterministic rules where required**

---

## 6. Enforcement

- The Scrum Master ensures DoR is respected before sprint work begins
- The Product Owner validates DoD before accepting stories
- QA ensures all quality criteria are met
- Developers are responsible for technical completeness

---

## 7. Decision Statement

The Beat-Bot team commits to enforcing DoR and DoD to ensure:

- High-quality delivery
- Reliable and trustworthy system behavior
- Alignment with stakeholder expectations

No story is started without being **Ready**, and no story is completed until it is **Done**.

---
