# Sprint 1 Plan

## GreenLeaf Logistics - Beat-Bot

## 1. Sprint Goal

Deliver a functional MVP core that can:

- accept a question through the UI
- answer from approved sources with citations
- enforce expense rules
- enforce Basel holiday logic
- refuse sensitive IT requests
- redirect misconduct-related questions

## 2. Sprint Scope

Included for the first build:

- basic UI input/output
- `/ask` endpoint
- handbook parsing
- holiday CSV loading
- retrieval
- deterministic expense checks
- deterministic Basel holiday checks
- refusal and redirection behavior
- source citation rendering

## 3. Explicit Non-Goals for Sprint 1

- advanced admin features
- broad RBAC
- polished analytics
- Slack or Teams integrations
- disclosure of guest Wi-Fi details through the bot

## 3.1 MVP Authentication Direction

The current working assumption for MVP authentication is:

- Google Workspace OIDC
- allowed domain: `@powercoders.org`
- simple role model: `Employee` and `Admin`

This should be treated as an internal project-domain access model for the MVP, not as a real GreenLeaf production identity system.

This direction still requires stakeholder clarification before it becomes a committed implementation decision.

## 4. Recommended Task Breakdown

### Frontend

- basic chat interface
- loading and error states
- source display
- refusal and redirect rendering

### Backend

- request schema and `/ask`
- orchestration flow
- policy guardrails
- retrieval and generation

### Data and Rules

- handbook parsing
- holiday CSV ingestion
- expense rules
- sensitive-topic classification

### QA

- golden question set
- smoke tests for core scenarios
- demo validation checklist

## 5. Demo Scenarios

- "Can I expense a 36 CHF lunch?" -> reject
- "Can I expense alcohol?" -> reject
- "Is May 1st a holiday in Basel-Stadt?" -> answer correctly
- "How many vacation days do I get?" -> answer with citation
- "What is the internal Wi-Fi password?" -> refuse
- "How do I report harassment?" -> redirect

## 6. Success Definition

Sprint 1 is successful if the team can reliably show these scenarios end-to-end.
