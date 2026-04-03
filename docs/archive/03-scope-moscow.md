# Scope and MoSCoW Prioritization

## GreenLeaf Logistics - Beat-Bot

## 1. Scope Position

Beat-Bot is a focused internal assistant for company policies. It is not a full HR system, a help desk replacement, or a general chatbot.(handbook reference)

## 2. Must Have

- Allow users to ask questions in natural language through a simple interface
- Provide answers based only on approved documents (handbook, Holiday tables)
- Refuse to answer when the information is unclear or not supported
- Do not respond to sensitive IT or credential-related questions
- Show clear answers with sources included (Citation)
- Handle unknown questions, harassment, bullying, and whistleblowing safely with a clear fallback response
- Respond Questions only based on Basel-stadt calendar
- User authentication

## 3. Should Have

- Admin pannel for admin control
- Short and professional conversational polish
- Log user questions and system responses (Query and response logging)
- Alignment with compnay's color palette

## 4. Could Have

- Limited multi-turn clarification
- Suggested follow-up questions

## 5. Won't Have

- Salary or compensation processing
- Full HR case management
- Logistics tracking
- External system integrations
- Self-service Wi-Fi password disclosure
- MAC registration detail disclosure

## 6. Included Topic Areas for MVP

- Expenses and travel
- Holidays
- Vacation and special leave
- Working hours and office rules (e.g., kitchen, fridge, etc.)
- Security refusal cases

## 8. Scope Guardrails

- If unsure(not in the resources), do not answer
- If the topic is sensitive, refuse or redirect
- If the answer cannot be cited, do not generate answers
