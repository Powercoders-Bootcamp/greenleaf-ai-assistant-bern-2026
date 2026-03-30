# Open Questions and Working Assumptions

## GreenLeaf Logistics - Beat-Bot

## 1. Purpose

This document now separates:

- decisions already locked
- questions that still need clarification
- recommended defaults for unresolved items

## 2. Decisions Already Locked

The following MVP decisions are already confirmed:

- user login is required
- the role model is `Employee` and `Admin`
- role mapping should live in the application database
- app access is identity-based only for now
- the system will not use keyword-based pre-classification or template-first routing
- the system will use LLM-first answer drafting with post-generation validation
- the bot should refuse all Wi-Fi password questions for now
- the bot should refuse MAC address registration details for now
- a source document may contain information that still must not be disclosed
- expense handling is text-only for MVP
- the system may rely on user declaration for external-client presence
- `Admin` can view all employee chat histories and related metadata
- each `Employee` can view only their own chat history
- chat history and related metadata should be persisted
- voice input is out of MVP scope for now
- multilingual support is out of MVP scope for now

## 3. Remaining Clarification Questions

1. Which concrete auth provider or login mechanism should the MVP use?
2. Are office etiquette topics part of MVP scope, or should the team focus only on high-value policy topics?
3. What citation format should the MVP use in the UI?
4. What exact retention window should apply to persisted chat history and metadata?
5. Should sensitive content inside chat history be masked, partially redacted, or stored as-is for admin review?

## 4. Recommended Defaults for Unresolved Items

Until clarified otherwise, the safest working defaults are:

- keep the MVP focused on high-value policy topics, not office etiquette
- use `document name + section title + page number when available` as the citation format
- keep retention short for MVP, such as 30 days
- mask or minimize obviously sensitive technical details in logs where practical

## 5. Short Stakeholder Prompts

- Which login mechanism should we implement for MVP if Google Workspace OIDC is not the current choice?
- Do you want office etiquette topics in MVP, or should we focus only on high-value policy questions such as expenses, holidays, leave, and safety?
- For citations, is `document + section + page` enough, or do you also want a short supporting snippet?
- How long should employee chat history and metadata be retained?
- Should admin-visible chat history ever redact sensitive content?
