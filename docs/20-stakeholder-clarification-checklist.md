# Stakeholder Clarification Checklist

## GreenLeaf Logistics - Beat-Bot

## Purpose

This checklist captures the most important questions the team should ask the stakeholder before implementation moves too far.

The goal is to confirm security, scope, authentication, and decision-making assumptions early.

## Identity and Access

- Should MVP login use the current project-domain setup with `@powercoders.org`, or is a `@greenleaf.com`-style company domain expected?
- Is Google Workspace OIDC acceptable for the MVP?
- Is a lightweight project login acceptable for demo purposes, or is a more realistic company-style login expected?
- What should `Admin` be able to do that `Employee` cannot do in the MVP?

## Security and Disclosure

- Should the bot refuse all Wi-Fi password questions in the MVP, including guest Wi-Fi?
- Is it acceptable for the bot to answer only with safe IT guidance such as "contact Sarah Muller in IT"?
- What exact level of detail is acceptable for MAC address registration questions?
- Are there any other technical or internal access topics that must always be refused?

## Expense Handling

- Will users type expense details manually, or should receipt upload be part of the MVP?
- If users ask general expense questions without enough detail, should the bot ask follow-up questions?
- Should the bot rely on user declaration for "at least one external client was present"?
- Must the bot require attendee count before making a per-person expense decision?

## Holiday and Policy Logic

- Is the holiday CSV the final source of truth for Basel-Stadt holiday logic in the MVP?
- Are there any holiday edge cases beyond May 1 that must be demonstrated?
- Are office etiquette topics part of MVP scope, or should the team focus only on high-value policy topics?

## Sensitive Conduct and HR Boundaries

- Is ombudsman redirection sufficient for harassment, bullying, and whistleblowing questions?
- Are there any other HR-sensitive topics that should always be redirected rather than answered?
- Should the bot answer only direct handbook leave rules, or also ask clarifying questions for ambiguous personal cases?

## Citations and User Experience

- What citation format is expected by the stakeholder:
  - section title only
  - section title plus page
  - short supporting snippet
- Is a simple chat UI enough for MVP, or is more structure expected in the answer layout?

## Delivery and MVP Scope

- Are the four core MVP capabilities acceptable as the main success criteria:
  - source-backed handbook Q&A
  - expense decisions
  - Basel-Stadt holiday logic
  - safe refusal and redirection
- Which optional features should definitely not be included in the 3-week MVP?
- Is receipt OCR considered MVP scope or post-MVP scope?

## Recommended Questions to Resolve First

The most important questions to confirm first are:

1. Which email/domain setup should be used for MVP login?
2. Should guest Wi-Fi password disclosure be blocked in the MVP?
3. Will expense handling be text-only, or include receipt upload?
4. What are the exact Admin vs Employee differences?
5. What citation detail level is expected?
