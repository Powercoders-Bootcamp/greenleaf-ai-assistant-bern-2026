# GreenLeaf AI Assistant

## Project Goal

Build an internal AI assistant for GreenLeaf Logistics that answers repetitive employee questions based strictly on approved company sources.

## Problem

Employees repeatedly ask HR and Operations the same questions about holidays, expenses, leave, attendance, and company rules. This creates avoidable interruptions and reduces productivity for Beat Muller and the operations team.

## Approved Sources

Current source set for the project:

- `GreenLeaf Logistics Internal Handbook v2.1`
- `Stakeholder Briefing: The "Beat-Bot" Project`
- `2026 Holiday Logic (CSV)`

## Proposed Solution

We are building a reliable internal assistant that:

- answers only from approved sources
- avoids hallucinations
- shows the source of each answer
- enforces deterministic rules for expenses and holiday logic
- redirects misconduct cases to the external ombudsman
- does not expose sensitive information

## Important Security Interpretation

The handbook includes guest Wi-Fi details, but the stakeholder requirement is stricter than raw source visibility. For the MVP:

- internal Wi-Fi credentials must never be disclosed
- MAC address registration details must not be disclosed
- the guest Wi-Fi password should not be disclosed through the bot
- users should be redirected to IT or the appropriate human-managed access process

## Key Requirements

- Accurate expense validation
- Basel-Stadt holiday accuracy
- Security-first behavior
- Proof of source
- Clear refusal behavior when confidence is low
- Clear project scope and team workflow

## Repository Structure

- `docs/` project documentation
- `data/` source and processed project data
- `src/` technical structure for future implementation

## MVP Focus

- source-backed policy Q&A
- deterministic expense decisions
- deterministic Basel holiday logic
- security refusal and redirection behavior
