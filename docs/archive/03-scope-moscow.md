# Scope and MoSCoW Prioritization

## GreenLeaf Logistics - Beat-Bot

## 1. Scope Position

Beat-Bot is a focused internal assistant for company policies. It is not a full HR system, a help desk replacement, or a general chatbot.

## 2. Must Have

- Allow users to ask questions in natural language through a simple interface
- Provide answers based only on approved documents
- Refuse to answer when the information is unclear or not supported
- Do not respond to sensitive IT or credential-related questions
- Redirect harassment, bullying, and whistleblowing questions to the ombudsman
- Show clear answers with sources included
- Handle unknown questions safely with a clear fallback response

## 3. Should Have

- User authentication
- Role-aware behavior (User - Admin)
- Clear refusal and redirection UX
- Log user questions and system responses (Query and response logging)
- Evaluate answers using predefined test questions (Basic evaluation with golden questions)

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
- Working hours and office rules (e.g., kitchen, fridge, etc.)
- Security refusal cases

## 7. Excluded or Restricted Topic Areas

- Internal credentials
- Device-registration details
- Sensitive misconduct handling
- Legal judgments outside the handbook
- Complex case-by-case HR decisions

## 8. Scope Guardrails

- If unsure, do not answer
- If the topic is sensitive, refuse or redirect
- If the answer cannot be cited, do not treat it as trusted

## 9. MVP Cut Line

For the 3-week delivery window, the team should optimize for:

- expense correctness
- Basel holiday correctness
- source citation quality
- refusal safety

