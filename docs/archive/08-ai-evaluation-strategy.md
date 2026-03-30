# AI Evaluation Strategy

> Archive note: This is a historical evaluation summary. It has been lightly updated to match the current LLM-first architecture.

## GreenLeaf Logistics - Beat-Bot

## 1. Evaluation Priorities

- policy correctness
- citation correctness
- refusal correctness
- redirect correctness
- consistency on repeated runs

## 2. Critical Evaluation Scenarios

- reject 36 CHF lunch
- reject alcohol expense
- answer May 1 correctly for Basel-Stadt
- answer vacation allowance with citation
- refuse internal and guest Wi-Fi password requests
- refuse MAC registration detail requests
- redirect harassment, bullying, and whistleblowing questions

## 3. Failure Analysis

When a case fails, classify the cause as:

- retrieval failure
- prompt failure
- validator failure
- data/source interpretation failure

## 4. Success Threshold

The MVP should not be considered trustworthy unless critical cases pass reliably, especially:

- expense decisions
- Basel holiday decisions
- sensitive IT refusals
- misconduct redirects
