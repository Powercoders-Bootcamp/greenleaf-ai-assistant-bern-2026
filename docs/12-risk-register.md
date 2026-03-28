# Risk Register

## GreenLeaf Logistics - Beat-Bot

| ID | Category | Risk | Likelihood | Impact | Priority | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Technical | Retrieval returns irrelevant or incomplete context | Medium | High | High | Section-aware chunking, metadata filtering, retrieval evaluation |
| R2 | Technical | LLM produces unsupported answers or fabricated citations | Medium | High | High | Source-only prompts, output validation, refusal fallback |
| R3 | Product | Expense rules are not enforced deterministically | Medium | High | High | Rule engine for 35 CHF and alcohol cases |
| R4 | Product | Basel-Stadt holiday logic is implemented incorrectly | Medium | High | High | Deterministic holiday logic from CSV plus tests |
| R5 | Security | Bot discloses Wi-Fi credentials or MAC registration details | Medium | High | High | Conservative refusal policy and IT redirection |
| R6 | Security | Team treats source visibility as universal permission to disclose | Medium | High | High | Security policy that overrides raw document recall for access topics |
| R7 | Product | Misconduct questions are handled as normal Q&A | Low | High | High | Explicit redirect logic to ombudsman |
| R8 | Team | Scope creep dilutes the MVP | High | High | High | Stay focused on expense, holidays, citations, and refusals |
| R9 | Technical | Weak test coverage misses critical regressions | Medium | Medium | Medium | Golden question set and manual QA checklist |
| R10 | Delivery | Team spends too much time on UI polish or auth depth | Medium | Medium | Medium | Defer non-core enhancements until core trust behavior works |

## Top Priority Risks

- R1 retrieval quality
- R2 hallucination and citation failure
- R3 expense-rule failure
- R4 Basel holiday failure
- R5 sensitive IT disclosure
- R8 scope creep

## Current Product Stance

Until explicit stakeholder approval exists, the project should treat guest Wi-Fi password disclosure as out of scope for the MVP bot experience.
