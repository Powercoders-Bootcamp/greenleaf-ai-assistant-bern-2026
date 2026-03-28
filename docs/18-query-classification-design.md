# Query Classification Design

## GreenLeaf Logistics - Beat-Bot

## Purpose

This document defines how Beat-Bot should classify user questions before policy checks, retrieval, and answer generation.

## Design Decision

Beat-Bot should use a **hybrid query-classification approach**:

1. deterministic rule and keyword pass
2. lightweight classifier pass only when needed
3. policy-based routing based on the final classification result

## Why This Approach

Pure keyword matching is too brittle for paraphrased user questions.

Pure LLM-based routing is unnecessarily risky and expensive for obvious high-signal cases.

The hybrid approach gives the team:

- deterministic behavior on obvious cases
- flexibility on paraphrased or ambiguous cases
- lower cost than sending every query to a model for routing
- safer handling of high-risk domains

## Step 1: Deterministic Pass

The first pass should use:

- keywords
- phrase matching
- basic heuristics
- simple regex or pattern rules where useful

### Example Signals

#### Expense

- expense
- receipt
- reimburse
- lunch
- alcohol
- CHF

#### Holiday and Leave

- holiday
- vacation
- leave
- May 1
- Basel
- bereavement

#### IT and Security

- Wi-Fi
- password
- MAC
- device registration
- login

#### Sensitive Conduct

- harassment
- bullying
- whistleblowing
- ombudsman

## Step 2: Lightweight Classifier

If the first pass does not produce a confident route, the system may run a lightweight classifier.

This classifier should:

- choose only from a fixed label set
- return structured labels
- not generate a free-form answer

## Recommended Output Schema

```json
{
  "domain": "expense | holiday | leave | office_policy | it_security | sensitive_conduct | unsupported",
  "question_type": "rule_based | informational | sensitive | unsupported",
  "sensitive": true,
  "needs_clarification": false,
  "routing_path": "policy_first | retrieval_generation | refuse | redirect"
}
```

## Example

User question:

`Can you tell me whether I can expense my lunch receipt?`

Classification:

```json
{
  "domain": "expense",
  "question_type": "rule_based",
  "sensitive": false,
  "needs_clarification": true,
  "routing_path": "policy_first"
}
```

## Recommended Routing Rules

### Route to `policy_first`

Use when:

- expense rules are involved
- holiday rules are involved
- the question touches sensitive IT access topics

In this path, the next response may be:

- a template-based clarification request
- a deterministic decision
- a template-based refusal
- a template-based redirect

### Route to `retrieval_generation`

Use when:

- the question is a normal handbook explanation request
- source-backed clarification is needed
- no refusal or deterministic decision is required first

### Route to `refuse`

Use when:

- the topic asks for restricted technical access details
- the question requests unsafe disclosures
- evidence is insufficient for a safe answer

### Route to `redirect`

Use when:

- the question is about harassment
- the question is about bullying
- the question is about whistleblowing

## Implementation Notes

- Start with a small, explicit label set
- Prefer deterministic routing when obvious signals exist
- Use the classifier as a fallback, not as the default for every query
- Log classification results for debugging and evaluation
- Add golden test questions for each domain

## Related Response Strategy

Classification and response strategy should work together:

- `policy_first` domains should prefer templates for clarification and deterministic outcomes
- `refuse` and `redirect` paths should use templates
- `retrieval_generation` should be used mainly for supported handbook explanation questions
