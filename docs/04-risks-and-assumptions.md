# Risks and Assumptions

## GreenLeaf Logistics - Beat-Bot

## 1. Core Assumptions

- The handbook and stakeholder briefing are the current source of truth for MVP behavior
- The most valuable questions are repetitive policy questions, not complex HR cases
- A narrow MVP is more valuable than a broad but unreliable assistant
- Retrieval quality can be acceptable if chunking and metadata are handled carefully

## 2. Critical Risks

### R1 - Retrieval quality risk

If retrieval returns weak context, the assistant may answer incorrectly or with weak citations.

### R2 - Hallucination risk

If the model answers beyond evidence, trust will collapse quickly.

### R3 - Holiday logic risk

If Basel-Stadt handling is wrong, the product will fail a core sponsor requirement.

### R4 - Expense policy risk

If 35 CHF and alcohol rules are not enforced deterministically, the product will fail a core sponsor requirement.

### R5 - Security interpretation risk

The handbook includes guest Wi-Fi details, but the stakeholder wants stronger disclosure controls. If this is handled loosely, the bot may leak information the sponsor considers unsafe.

### R6 - Scope creep risk

The handbook contains many low-value topics. If the team tries to cover everything equally, the MVP may become late and unreliable.

## 3. Risk Mitigations

- Use deterministic rules for expenses and holidays
- Require source-backed answers
- Refuse when confidence or grounding is weak
- Treat Wi-Fi and MAC registration questions conservatively in the MVP
- Prioritize a small golden question set early
- Cut optional features before cutting safety controls

## 4. Key Product Assumption to Validate

The team is currently assuming that guest Wi-Fi passwords should not be disclosed through the bot in the MVP, even if present in source material. This is the safest interpretation, but it should be validated with the stakeholder if more permissive behavior is ever desired.
