# Risk Register

> Archive note: This is a historical risk register. Terminology has been lightly updated to match the current validator-based architecture.

## GreenLeaf Logistics - Beat-Bot

| ID | Category | Risk | Likelihood | Impact | Priority | Mitigation |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Technical | Retrieval returns irrelevant or incomplete context | Medium | High | High | Section-aware chunking, metadata filtering, retrieval evaluation |
| R2 | Technical | LLM produces unsupported answers or fabricated citations | Medium | High | High | Source-only prompting, output validation, refusal fallback |
| R3 | Product | Expense rules are not enforced correctly by the validator layer | Medium | High | High | Structured fact extraction plus consistency checks for 35 CHF and alcohol cases |
| R4 | Product | Basel-Stadt holiday logic is implemented incorrectly | Medium | High | High | Deterministic holiday logic from CSV plus tests |
| R5 | Security | Bot discloses Wi-Fi credentials or MAC registration details | Medium | High | High | Conservative refusal policy and IT redirection |
| R6 | Security | Team treats source visibility as universal permission to disclose | Medium | High | High | Security policy that overrides raw document recall for access topics |
| R7 | Product | Misconduct questions are handled as normal Q&A | Low | High | High | Explicit response-type validation and safe redirect logic |
| R8 | Team | Scope creep dilutes the MVP | High | High | High | Stay focused on expense, holidays, citations, and refusals |
| R9 | Technical | Weak test coverage misses critical regressions | Medium | Medium | Medium | Golden question set and manual QA checklist |
| R10 | Delivery | Team spends too much time on UI polish or auth depth | Medium | Medium | Medium | Defer non-core enhancements until core trust behavior works |
| R11 | Privacy | Too much user data or chat history is exposed to the model | Medium | High | High | Backend-controlled minimum-context prompting and strict access boundaries |
