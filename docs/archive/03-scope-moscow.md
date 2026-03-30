# Scope and MoSCoW Prioritization

## GreenLeaf Logistics - Beat-Bot

## 1. Scope Position

Beat-Bot is a narrow internal policy assistant. It is not a full HR system, not a help desk replacement, and not a general conversational bot.

## 2. Must Have

- Ask a question in natural language through a simple UI
- Return source-backed answers from approved documents
- Refuse low-confidence or unsupported questions
- Refuse sensitive IT and credential-related questions
- Redirect harassment, bullying, and whistleblowing questions to the ombudsman
- Return structured answers with citations

## 3. Should Have

- User authentication
- Role-aware behavior (User - Admin)
- Clear refusal and redirection UX
- Query and response logging
- Basic evaluation with golden questions

## 4. Could Have

- Friendly conversational polish
- Limited multi-turn clarification
- Admin review visibility
- Usage analytics
- Suggested follow-up questions

## 5. Won't Have

- Salary or compensation processing
- Full HR case management
- Logistics tracking
- External system integrations
- Self-service Wi-Fi password disclosure
- MAC registration detail disclosure
- Autonomous workflow execution

## 6. Included Topic Areas for MVP

- Expenses and travel
- Holidays
- Vacation and special leave
- Basic attendance and office policy questions
- Security refusal cases

## 7. Excluded or Restricted Topic Areas

- Internal credentials
- Device-registration details
- Sensitive misconduct handling
- Legal judgments outside the handbook
- Complex case-by-case HR decisions

## 8. Scope Guardrails

- When in doubt, do not answer
- If the topic is sensitive, refuse or redirect
- If the answer cannot be cited, do not treat it as trusted

## 9. MVP Cut Line

For the 3-week delivery window, the team should optimize for:

- expense correctness
- Basel holiday correctness
- source citation quality
- refusal safety

UI polish and advanced access-control depth should come after these.
