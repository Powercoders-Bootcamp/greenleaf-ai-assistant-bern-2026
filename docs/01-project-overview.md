# Project Overview

## GreenLeaf Logistics - Beat-Bot

## 1. Project Summary

Beat-Bot is an internal AI assistant for GreenLeaf Logistics. Its goal is to reduce repetitive questions from employees by answering them automatically using the company handbook and provided data.

The bot focuses on common topics like expenses, holidays, and leave. It should give clear and accurate answers and always refer to the source in the handbook.

It is not a general chatbot and it focuses only on a few important topics, like expenses, holidays, and leave policies, and aims to handle them in a simple and reliable way.

## 2. Business Problem

Beat Müller, Head of Operations & HR, is repeatedly interrupted by employees asking the same questions:

- Is May 1st a holiday in Basel-Stadt?
- Can I expense this lunch?
- How much leave do I get?
- What does the handbook say about attendance or office rules?

The handbook already contains the answers, but employees do not reliably find or interpret them.

## 3. Product Goal

The goal of this project is to build a reliable assistant that:

- only answers using approved sources
- shows where each answer comes from
- follows company rules strictly (no exceptions)
- does not answer sensitive questions
- does not guess or make up information

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

- Internal Wi-Fi access is only given to registered devices and must be approved by Sarah Müller from IT
- A guest Wi-Fi password exists, but it is managed internally and changed regularly

However, the stakeholder requirement is stricter than simple document recall. For the MVP, Beat-Bot should:

- refuse requests for internal Wi-Fi credentials
- refuse requests for guest Wi-Fi passwords
- refuse requests for MAC address registration details
- safely direct users to IT when access help is needed
- not confirm or validate any shared credentials

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
- give answers with handbook references
- safe refusal on sensitive IT questions
- safe redirection for misconduct questions (Exp:“For this kind of issue, please contact our confidential ombudsman at ombudsman@greenleaf-safety.ch)

## 12. Delivery Position

This MVP can be done in 3 weeks if we focus on the essentials and prioritize safety and correct answers.