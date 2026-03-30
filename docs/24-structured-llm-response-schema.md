# Structured LLM Response Schema

## GreenLeaf Logistics - Beat-Bot

## 1. Purpose

This document defines the recommended structured response format for the LLM-first MVP architecture.

The goal is to:

- avoid relying on raw free-text alone
- make backend validation easier and safer
- support retries and safe fallbacks

## 2. Design Principle

The LLM should return a structured draft object.

The backend should:

- validate the object
- decide whether it is safe to release
- retry or fall back if needed

## 2.1 Best-Practice Summary

The recommended implementation approach for this project is:

- use structured LLM output instead of trusting raw free text
- keep the schema small and practical
- validate fields, not prose, whenever possible
- treat the backend as the release authority
- keep generation and validation as separate responsibilities
- use narrow deterministic validators for high-risk domains
- log validator outcomes for auditability
- never trust model self-report fields alone for safety-critical decisions
- prefer safe fallback over risky confidence
- keep identity, role, and full-history access outside the model boundary

## 3. Recommended Top-Level Schema

```json
{
  "answer_text": "You cannot expense this lunch because the amount exceeds the allowed limit.",
  "response_type": "policy_answer",
  "decision": "reject",
  "needs_clarification": false,
  "clarification_fields": [],
  "sensitive_topic": false,
  "detected_topics": ["expense"],
  "facts": {
    "amount_total": 36.0,
    "currency": "CHF",
    "people_count": 1,
    "amount_per_person": 36.0,
    "alcohol_present": false,
    "external_client_present": true,
    "date": null,
    "region": null
  },
  "citations": [
    {
      "document": "Handbook GreenLeaf Logistics",
      "section": "Expenses & Travel",
      "page": 7
    }
  ],
  "validator_hints": {
    "contains_credentials": false,
    "contains_restricted_technical_detail": false,
    "expected_followup_required": false
  }
}
```

## 4. Required Fields

These fields should always be present:

- `answer_text`
- `response_type`
- `decision`
- `needs_clarification`
- `clarification_fields`
- `sensitive_topic`
- `detected_topics`
- `facts`
- `citations`
- `validator_hints`

## 5. Field Definitions

### `answer_text`

User-facing natural-language draft.

This is never released without validation.

### `response_type`

Allowed MVP values:

- `policy_answer`
- `handbook_answer`
- `clarification`
- `refusal`
- `redirect`
- `verification_failure`

### `decision`

Allowed MVP values:

- `allow`
- `reject`
- `inform`
- `clarify`
- `refuse`
- `redirect`
- `unknown`

This field is useful because validators can inspect the decision directly instead of trying to infer it from prose.

### `needs_clarification`

Boolean flag.

If `true`, the backend should expect a clarification-oriented response or a safe follow-up prompt.

### `clarification_fields`

Array of missing fields the model believes are required.

Examples:

- `amount_total`
- `people_count`
- `alcohol_present`
- `external_client_present`
- `date`
- `region`

### `sensitive_topic`

Boolean flag indicating whether the draft concerns a high-risk area such as:

- Wi-Fi credentials
- MAC registration
- harassment
- bullying
- whistleblowing

### `detected_topics`

Array of coarse topics.

Examples:

- `expense`
- `holiday`
- `leave`
- `security`
- `misconduct`
- `handbook_general`

### `facts`

Structured facts extracted by the model from the question and source context.

Recommended MVP fields:

- `amount_total`
- `currency`
- `people_count`
- `amount_per_person`
- `alcohol_present`
- `external_client_present`
- `date`
- `region`

The backend should prefer these fields over brittle text parsing when applying validators.

### `citations`

Array of citation objects.

Each item should contain:

- `document`
- `section`
- `page`

For MVP, the recommended citation display format is:

- `document name + section title + page number when available`

### `validator_hints`

Optional model-supplied hints for validation support.

Recommended MVP fields:

- `contains_credentials`
- `contains_restricted_technical_detail`
- `expected_followup_required`

These hints are advisory only. The backend must not trust them blindly.

## 6. Example Outputs by Scenario

### Expense Rejection

```json
{
  "answer_text": "No. This lunch is above the 35 CHF per person limit.",
  "response_type": "policy_answer",
  "decision": "reject",
  "needs_clarification": false,
  "clarification_fields": [],
  "sensitive_topic": false,
  "detected_topics": ["expense"],
  "facts": {
    "amount_total": 36.0,
    "currency": "CHF",
    "people_count": 1,
    "amount_per_person": 36.0,
    "alcohol_present": false,
    "external_client_present": true,
    "date": null,
    "region": null
  },
  "citations": [
    {
      "document": "Handbook GreenLeaf Logistics",
      "section": "Expenses & Travel",
      "page": 7
    }
  ],
  "validator_hints": {
    "contains_credentials": false,
    "contains_restricted_technical_detail": false,
    "expected_followup_required": false
  }
}
```

### Expense Clarification

```json
{
  "answer_text": "I can help, but I need the total amount, number of people, whether alcohol was included, and whether at least one external client was present.",
  "response_type": "clarification",
  "decision": "clarify",
  "needs_clarification": true,
  "clarification_fields": [
    "amount_total",
    "people_count",
    "alcohol_present",
    "external_client_present"
  ],
  "sensitive_topic": false,
  "detected_topics": ["expense"],
  "facts": {
    "amount_total": null,
    "currency": "CHF",
    "people_count": null,
    "amount_per_person": null,
    "alcohol_present": null,
    "external_client_present": null,
    "date": null,
    "region": null
  },
  "citations": [],
  "validator_hints": {
    "contains_credentials": false,
    "contains_restricted_technical_detail": false,
    "expected_followup_required": true
  }
}
```

### Wi-Fi Refusal

```json
{
  "answer_text": "I can't share Wi-Fi passwords or MAC registration details. Please contact IT.",
  "response_type": "refusal",
  "decision": "refuse",
  "needs_clarification": false,
  "clarification_fields": [],
  "sensitive_topic": true,
  "detected_topics": ["security"],
  "facts": {
    "amount_total": null,
    "currency": null,
    "people_count": null,
    "amount_per_person": null,
    "alcohol_present": null,
    "external_client_present": null,
    "date": null,
    "region": null
  },
  "citations": [],
  "validator_hints": {
    "contains_credentials": false,
    "contains_restricted_technical_detail": false,
    "expected_followup_required": false
  }
}
```

### Misconduct Redirect

```json
{
  "answer_text": "Please use the confidential ombudsman process for this issue.",
  "response_type": "redirect",
  "decision": "redirect",
  "needs_clarification": false,
  "clarification_fields": [],
  "sensitive_topic": true,
  "detected_topics": ["misconduct"],
  "facts": {
    "amount_total": null,
    "currency": null,
    "people_count": null,
    "amount_per_person": null,
    "alcohol_present": null,
    "external_client_present": null,
    "date": null,
    "region": null
  },
  "citations": [
    {
      "document": "Handbook GreenLeaf Logistics",
      "section": "Sensitive Matters & Conduct",
      "page": 9
    }
  ],
  "validator_hints": {
    "contains_credentials": false,
    "contains_restricted_technical_detail": false,
    "expected_followup_required": false
  }
}
```

## 7. Validator Expectations

### Schema Validator

Checks:

- required fields exist
- enum-like fields use allowed values
- arrays and objects have expected shapes

### Citation Validator

Checks:

- `policy_answer` and `handbook_answer` should normally include citations
- citation objects contain document/section metadata

### Disclosure Validator

Checks:

- no credential leakage
- no actionable MAC registration detail
- safe refusal text is allowed

Important:

- do not block the phrase `MAC address` everywhere
- only block actionable disclosure, not refusal wording

### Consistency Validator

Checks high-risk fields using structured facts.

Examples:

- if `amount_per_person > 35`, `decision` must not be `allow`
- if `alcohol_present = true`, `decision` must not be `allow`
- if `date = 2026-05-01` and `region = Basel-Stadt`, the draft must not deny the holiday

### Response-Type Validator

Checks:

- Wi-Fi/password/MAC requests should end in `refusal`
- harassment/bullying/whistleblowing should end in `redirect`

## 8. Retry and Fallback Rules

If validation fails:

1. retry once with a stricter instruction when the failure looks recoverable
2. if the second draft still fails, return a safe fallback

Recommended safe fallbacks:

- `refusal` for restricted technical disclosure
- `redirect` for misconduct topics
- `verification_failure` when a trustworthy answer cannot be confirmed

## 9. Implementation Notes

- keep the schema small enough for reliable model output
- add fields only when validators truly need them
- prefer typed backend parsing with Pydantic or equivalent
- store validator outcomes in audit logs
- never rely on model self-report fields alone for safety-critical release decisions

## 10. Anti-Patterns to Avoid

Avoid these implementation patterns:

- trusting raw answer text without a structured schema
- blocking or approving answers with naive substring rules alone
- letting the same layer both generate and approve the response
- using oversized schemas with many rarely used fields
- relying only on model self-reported safety flags
- returning a risky draft when validation is inconclusive
- giving the model broad access to user records, role mapping, or full conversation history by default
