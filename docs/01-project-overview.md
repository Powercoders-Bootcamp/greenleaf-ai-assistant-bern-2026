# Project Overview

## GreenLeaf Logistics - Beat-Bot

## 1. Project Summary

Beat-Bot is an internal AI assistant for GreenLeaf Logistics. Its purpose is to reduce repetitive operational interruptions by answering employee handbook questions with source-backed responses while refusing unsafe or unsupported requests.

The product is not intended to behave like a general-purpose chatbot. It is a narrow, policy-aware assistant focused on a small number of high-value employee questions.

## 2. Business Problem

Beat Muller, Head of Operations & HR, is repeatedly interrupted by employees asking the same questions:

- Is May 1st a holiday in Basel-Stadt?
- Can I expense this lunch?
- How much leave do I get?
- What does the handbook say about attendance or office rules?

The handbook already contains the answers, but employees do not reliably find or interpret them.

## 3. Product Goal

The goal of the project is to deliver a reliable assistant that:

- answers from approved sources only
- cites the source of every trusted answer
- enforces hard policy rules deterministically
- refuses or redirects sensitive questions
- avoids hallucinations and unsupported guessing

## 4. Approved Source Set

The current project scope is grounded in:

- `GreenLeaf Logistics Internal Handbook v2.1`
- `Stakeholder Briefing: The "Beat-Bot" Project`
- `2026 Holiday Logic (CSV)`

## 5. Primary MVP Use Cases

The first version must perform well on the following:

- Expense questions
- Basel-Stadt holiday questions
- Vacation and leave questions
- General handbook Q&A with citations
- Sensitive-topic refusal and redirection

## 6. Hard Requirements from the Stakeholder

Beat's non-negotiable expectations are:

- If a lunch is above 35 CHF per person, the bot says no
- If alcohol is included, the bot says no
- Basel-Stadt holiday logic must be correct, especially May 1
- The bot must not expose sensitive IT information
- The bot must show where in the handbook it found the answer

## 7. Security Boundary Clarification

The handbook states that:

- internal staff Wi-Fi access requires MAC address registration with Sarah Muller in IT
- the guest Wi-Fi password exists and is rotated annually

However, the stakeholder requirement is stricter than simple document recall. For the MVP, Beat-Bot should:

- refuse requests for internal Wi-Fi credentials
- refuse requests for guest Wi-Fi passwords
- refuse requests for MAC address registration details
- safely direct users to IT when access help is needed

This conservative behavior reduces security risk and aligns with the stakeholder's trust threshold.

## 8. Sensitive Matter Handling

The handbook explicitly states that harassment, bullying, and whistleblowing should not be handled by the internal bot. These cases must be redirected to the external confidential ombudsman.

## 9. In Scope

- Internal handbook Q&A
- Source citation
- Expense rule enforcement
- Basel-specific holiday logic
- Vacation and leave guidance
- Refusal for unsafe or unsupported questions
- Redirection for misconduct-related topics
- Basic web UI and backend flow

## 10. Out of Scope

- Payroll and salary changes
- HR case handling
- Legal advice
- Logistics operations and tracking
- Self-service disclosure of Wi-Fi credentials
- Technical device-registration details
- Broad enterprise system integrations

## 11. Success Criteria

The MVP is successful if it can demonstrate:

- correct expense rejection behavior
- correct Basel holiday behavior
- source-backed handbook answers
- safe refusal on sensitive IT questions
- safe redirection for misconduct questions

## 12. Delivery Position

This is a realistic 3-week MVP only if the team stays narrow and prioritizes trust, safety, and correctness over breadth.
