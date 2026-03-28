# Open Questions Register

## GreenLeaf Logistics - Beat-Bot

## Purpose

This document lists the main open product and implementation questions that still need explicit decisions.

The goal is to make ambiguity visible early, reduce hidden scope creep, and help the team decide what must be clarified before implementation or demo.

## How to Use This Document

For each open question, the team should decide:

- whether a decision is needed for MVP
- who owns the decision
- what the default assumption is if no decision is made in time

## Open Questions

### OQ-01 - Should the bot ever disclose the guest Wi-Fi password?

**Why this matters**  
The handbook contains the guest Wi-Fi password, but the stakeholder briefing sets a stricter security expectation around Wi-Fi-related disclosures.

**Current safe MVP assumption**  
Do not disclose the guest Wi-Fi password through the bot.

**Decision needed**  
Should guest Wi-Fi remain fully blocked in MVP, or should it be disclosed only to explicitly authorized roles in a later version?

**Impact if unresolved**  
A weak decision here could create a security and trust problem.

### OQ-02 - How should the bot handle MAC address registration questions?

**Why this matters**  
The handbook says internal devices must be registered through IT, but the stakeholder does not want technical access details shared broadly.

**Current safe MVP assumption**  
Allow only safe process guidance such as "contact Sarah Muller in IT," and refuse operational or technical registration details.

**Decision needed**  
What exact level of detail is acceptable for device-registration help?

**Impact if unresolved**  
The bot may either overshare technical details or become less helpful than necessary.

### OQ-03 - Will users type expense details manually, or upload receipts?

**Why this matters**  
This changes the architecture, UI, testing scope, and delivery effort.

**Current safe MVP assumption**  
Users type expense questions and the system evaluates the described scenario.

**Decision needed**  
Will the MVP support receipt upload, OCR, and structured extraction, or only text-based expense questions?

**Impact if unresolved**  
The team may underestimate implementation effort or build the wrong input flow.

### OQ-04 - If receipt upload is added, how much OCR intelligence is required?

**Why this matters**  
There is a large difference between basic text extraction and reliable receipt understanding.

**Current safe MVP assumption**  
If upload is added, start with simple OCR plus rule checks for amount and alcohol, with fallback when extraction is uncertain.

**Decision needed**  
Should the system only extract raw text, or should it also parse totals, line items, and per-person calculations?

**Impact if unresolved**  
The team could overbuild or promise more receipt intelligence than can be delivered safely.

### OQ-05 - How is "at least one external client is present" verified?

**Why this matters**  
This is part of the expense rule, but it is not directly verifiable from the handbook alone.

**Current safe MVP assumption**  
Rely on user-provided information and clearly state that the answer depends on the declared scenario.

**Decision needed**  
Should the bot accept user declaration, ask a follow-up question, or avoid approval-style answers when client presence is unclear?

**Impact if unresolved**  
Expense decisions may appear more authoritative than the available evidence supports.

### OQ-06 - How should per-person expense limits be calculated?

**Why this matters**  
The rule is 35 CHF per person, but users may provide only a total amount.

**Current safe MVP assumption**  
If person count is missing, ask a clarifying question or refuse to make a final determination.

**Decision needed**  
Should the bot require explicit attendee count before making a per-person decision?

**Impact if unresolved**  
The system may produce incomplete or misleading expense outcomes.

### OQ-07 - What is the exact boundary between safe process guidance and restricted IT detail?

**Why this matters**  
Some IT-related answers are safe, while others are too operationally sensitive.

**Current safe MVP assumption**  
General contact guidance is allowed; technical access details are not.

**Decision needed**  
Which example questions are allowed:

- "Who handles device registration?"
- "How do I get Wi-Fi access?"
- "How do I register my MAC address?"

**Impact if unresolved**  
The team may implement inconsistent refusal behavior.

### OQ-08 - What can Admin do that Employee cannot do?

**Why this matters**  
The documents mention Employee and Admin roles, but the actual permission model is still shallow.

**Current safe MVP assumption**  
Admin is mainly a governance and review role, not a privileged recipient of sensitive credentials through the bot.

**Decision needed**  
Should Admin be able to:

- view logs
- review failure cases
- access analytics
- see evaluation results
- override restricted answers

**Impact if unresolved**  
Role-aware access control may remain vague and difficult to implement.

### OQ-09 - How much multi-turn conversation should the MVP support?

**Why this matters**  
Multi-turn support improves usability, but increases safety and consistency risk.

**Current safe MVP assumption**  
Support only limited clarification turns.

**Decision needed**  
Should the MVP support:

- single-turn only
- one or two follow-up questions
- broader conversational context

**Impact if unresolved**  
The team may overcomplicate prompt design and QA scope.

### OQ-10 - How detailed should citations be?

**Why this matters**  
The stakeholder wants proof of source, but the exact citation format has not been fully defined.

**Current safe MVP assumption**  
Show document name plus section title, and page number when available.

**Decision needed**  
Should citations include:

- section title only
- section title and page
- a short supporting snippet

**Impact if unresolved**  
The UI and backend may implement citation behavior that does not fully satisfy stakeholder expectations.

### OQ-11 - Which handbook topics are truly MVP-relevant?

**Why this matters**  
The handbook includes both high-value policy rules and low-value office trivia.

**Current safe MVP assumption**  
Prioritize expenses, holidays, leave, attendance basics, and sensitive-topic handling.

**Decision needed**  
Should office etiquette topics such as kitchen rules, microwave cleaning, fridge labels, and office plants be treated as MVP scope or backlog-later content?

**Impact if unresolved**  
The team may spend time polishing low-value knowledge while critical scenarios remain under-tested.

### OQ-12 - How strict should the system be on unsupported or ambiguous leave questions?

**Why this matters**  
Some leave questions are straightforward, but edge cases can invite over-interpretation.

**Current safe MVP assumption**  
Answer only what the handbook clearly supports, and avoid making discretionary HR judgments.

**Decision needed**  
Should the bot:

- answer only direct handbook cases
- ask clarifying questions
- redirect ambiguous personal cases to HR

**Impact if unresolved**  
The assistant may drift into unsupported HR judgment.

### OQ-13 - Should the stakeholder briefing itself be cited as a source in user-facing answers?

**Why this matters**  
Some stakeholder expectations drive behavior, but not all of them belong in user-facing policy explanations.

**Current safe MVP assumption**  
Use the stakeholder briefing mainly as a product and guardrail source, not as a primary user-facing citation unless necessary.

**Decision needed**  
When, if ever, should the stakeholder briefing appear in the citation layer shown to users?

**Impact if unresolved**  
User-facing answers may mix operational policy with project-level intent in a confusing way.

### OQ-14 - How much authentication is required beyond the chosen MVP setup?

**Why this matters**  
Authentication improves security but also increases delivery scope.

**Current safe MVP assumption**  
Use Google Workspace OIDC with approved `@powercoders.org` accounts.

**Decision needed**  
Does the MVP need anything beyond this, such as stronger role mapping or additional access restrictions?

**Impact if unresolved**  
The team may spend too much time on access mechanics instead of core trust behavior.

**Note to confirm explicitly**  
The team should still ask whether login for the MVP should use the project-domain setup with `@powercoders.org`, or whether a real or simulated `@greenleaf.com`-style company domain is expected by stakeholders.

### OQ-15 - What should happen when retrieval finds weak evidence but the question seems answerable?

**Why this matters**  
RAG systems often face cases where evidence is partial but not empty.

**Current safe MVP assumption**  
Prefer refusal or a cautious fallback over a confident but weakly grounded answer.

**Decision needed**  
What confidence threshold or validation rule should trigger refusal?

**Impact if unresolved**  
The assistant may become either too risky or too unhelpful.

## Recommended Priority for Decision-Making

The most important open questions to resolve before serious implementation are:

1. OQ-01 guest Wi-Fi disclosure policy
2. OQ-02 MAC address registration disclosure boundary
3. OQ-03 expense input model
4. OQ-05 client presence verification
5. OQ-06 per-person expense calculation
6. OQ-08 Admin vs Employee permissions
7. OQ-10 citation detail level

## Default Rule If a Decision Is Missing

If a question remains unresolved during MVP development:

- choose the safer behavior
- prefer refusal over risky disclosure
- prefer narrow scope over broad scope
- prefer deterministic answers over inferred ones
