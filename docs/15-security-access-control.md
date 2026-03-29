# Security and Access Control

## GreenLeaf Logistics - Beat-Bot

## 1. Security Objective

Beat-Bot must help users with policy questions without becoming a channel for disclosing sensitive technical or HR information.

## 2. Core Security Principle

Source presence does not equal disclosure permission.

If the handbook contains a sensitive operational detail, the bot still needs policy-level permission before revealing it.

## 3. Sensitive Categories for MVP

- internal Wi-Fi credentials
- guest Wi-Fi passwords
- MAC address registration details
- internal technical identifiers
- harassment, bullying, and whistleblowing cases

## 4. Allowed vs Restricted Behavior

### Allowed

- explain that internal Wi-Fi access is handled by IT
- direct users to Sarah Muller or the IT desk
- answer non-sensitive handbook questions with citations
- explain the ombudsman escalation path for misconduct

### Restricted

- disclose internal Wi-Fi passwords
- disclose the guest Wi-Fi password through the bot
- describe MAC address registration details beyond safe process guidance
- disclose confidential technical setup details
- conduct misconduct intake through the bot

## 5. MVP Access Policy for Wi-Fi and MAC Topics

For the first release:

- "What is the internal Wi-Fi password?" -> refuse
- "What is the guest Wi-Fi password?" -> refuse
- "How do I get connected?" -> provide safe process guidance
- "What MAC address do I need to register?" -> refuse
- "Who handles device registration?" -> answer with IT contact guidance

## 6. Role Model

The project currently distinguishes between:

- `Employee`
- `Admin`

However, the MVP should not rely on incomplete RBAC to justify disclosure of credentials. Sensitive access details should remain restricted even if basic roles exist.

## 6.1 MVP Authentication Approach

The current working assumption for MVP authentication is:

- Google Workspace OIDC
- approved user domain: `@powercoders.org`
- lightweight internal access control for project users only

This is a practical project setup for the MVP. It should not be confused with a real GreenLeaf production identity environment.

This remains subject to stakeholder clarification.

## 7. Security Controls

- authenticated access when available
- input validation
- query classification for sensitive topics
- refusal and redirect logic
- server-side logging with minimal sensitive content
- secrets managed outside source code

## 8. Future Extension

If the organization later wants role-based guest Wi-Fi disclosure, that behavior should only be added after:

- explicit stakeholder approval
- a written access rule
- auditable role checks
- dedicated tests

## 9. Security Decision

The MVP will use a conservative disclosure policy to protect trust and reduce the risk of accidental leakage.
