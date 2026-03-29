# Open Questions and Working Assumptions

## GreenLeaf Logistics - Beat-Bot

## 1. Purpose

This document combines:

- unresolved clarification questions
- current safe MVP assumptions
- short stakeholder-meeting prompts

It is the main place to track what is still undecided.

## 2. Working Assumptions

These are defaults only, not final commitments:

- use a narrow MVP scope
- prefer refusal over risky disclosure
- use text-first input for MVP
- keep expense and holiday logic deterministic
- use templates for clarification, refusal, redirect, and deterministic outcomes
- use retrieval plus generation for supported handbook explanations
- treat `Google Workspace OIDC + @powercoders.org` as a working auth assumption only
- keep persistent logs as a working assumption, with final retention/access rules still pending
- defer OCR and voice input unless explicitly prioritized

## 3. Highest-Priority Clarification Questions

1. Which login/domain setup should the MVP use?
2. Is Google Workspace OIDC acceptable for MVP auth?
3. Should the bot refuse all Wi-Fi password questions, including guest Wi-Fi?
4. If a sensitive detail exists in a source document, should the bot still refuse to disclose it?
5. What exact level of detail is acceptable for MAC address registration questions?
6. Will expense handling be text-only, or include receipt upload/OCR?
7. Should the bot rely on user declaration for external-client presence?
8. What can `Admin` do that `Employee` cannot do?
9. Where should role mapping live: app DB, config allowlist, or provider groups/claims?
10. Should the app keep persistent logs, and if yes, what should be stored, who can access it, and for how long?
11. Should app access depend only on identity, or also on managed/registered devices?
12. Is voice-message input in or out of MVP scope?

## 4. Security and Disclosure Questions

- Should the bot refuse all Wi-Fi password questions in the MVP?
- If a source document contains sensitive information, does security policy still override normal source-backed answering?
- What level of MAC registration explanation is safe?
- Are there any additional IT or access topics that must always be refused?

## 5. Expense and Input Questions

- Will expenses be handled through text only, or through receipt upload too?
- If receipt upload is added, how much OCR intelligence is actually expected?
- Should the bot ask follow-up questions when amount, person count, alcohol status, or external-client presence is missing?
- Should the bot rely on user declaration for external-client presence?
- Should per-person attendee count be mandatory before a decision is made?

## 6. Auth, Roles, and Access Questions

- Should MVP login use `@powercoders.org` project accounts or a company-style domain?
- Should app roles be stored in an app DB, config allowlist, or provider claims?
- Should app access be identity-based only, or require company-network or managed-device conditions?
- What extra visibility or power should `Admin` have, if any?

## 7. Logging and Data-Retention Questions

- Should logs be persistent?
- Should logs store full user questions, or only routing and policy metadata?
- Who should be allowed to view logs?
- How long should logs be retained?
- Should sensitive content be masked or excluded?

## 8. Scope and UX Questions

- Are office etiquette topics part of MVP scope, or should the team focus only on high-value policy topics?
- Should the MVP support multilingual input?
- Should the MVP support voice-message input?
- What citation format is expected:
  - section title only
  - section title plus page
  - short supporting snippet

## 9. Default Rule When a Decision Is Missing

If a clarification is still unresolved during MVP work:

- choose the safer behavior
- keep the scope narrower
- prefer deterministic decisions
- prefer refusal over risky disclosure
- treat recommended defaults as temporary only
