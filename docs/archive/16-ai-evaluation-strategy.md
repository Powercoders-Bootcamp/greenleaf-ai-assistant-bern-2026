# AI Evaluation Strategy

## GreenLeaf Logistics - Beat-Bot

## 1. Purpose

Beat-Bot must be evaluated as a policy assistant, not as a general conversational model.

## 2. Evaluation Priorities

- policy correctness
- citation correctness
- refusal correctness
- redirect correctness
- consistency on repeated runs

## 3. Critical Evaluation Scenarios

### Expense

- reject 36 CHF lunch
- reject alcohol expense

### Holidays

- answer May 1 correctly for Basel-Stadt
- answer national-holiday cases correctly

### General Handbook

- answer vacation allowance with citation
- answer bereavement leave with citation

### Security

- refuse internal Wi-Fi password requests
- refuse guest Wi-Fi password requests in MVP
- refuse MAC registration detail requests
- allow safe process guidance to IT

### Sensitive Conduct

- redirect harassment, bullying, and whistleblowing questions

## 4. Evaluation Metrics

- critical-case accuracy
- citation validity rate
- refusal accuracy
- redirect accuracy
- consistency rate

## 5. Failure Analysis

When a case fails, the team should classify the cause as one of:

- retrieval failure
- prompt failure
- policy-layer failure
- validation failure
- data/source interpretation failure

## 6. Success Threshold

The MVP should not be considered trustworthy unless critical cases pass reliably, especially:

- expense decisions
- Basel holiday decisions
- sensitive IT refusals
- misconduct redirects
