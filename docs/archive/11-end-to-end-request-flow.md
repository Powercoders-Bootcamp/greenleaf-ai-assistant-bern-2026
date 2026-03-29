# End-to-End Request Flow

## GreenLeaf Logistics - Beat-Bot

## 1. Step 1 - User submits a question

The user asks a question in the web UI.

Examples:

- "Can I expense a 36 CHF lunch?"
- "Is May 1st a holiday in Basel-Stadt?"
- "What is the internal Wi-Fi password?"

## 2. Step 2 - API validates the request

The backend validates:

- request format
- session information if enabled
- basic input safety rules

If optional helper processing is enabled in later phases, the request may also pass through:

- language detection
- translation into the system's working language
- transcription if the input started as audio

## 3. Step 3 - Query classification

The system classifies the question into one of the key domains:

- expenses
- holidays
- leave and handbook policy
- IT/security
- sensitive conduct
- unsupported

The recommended implementation is a hybrid flow:

1. deterministic keyword and pattern pass
2. lightweight classifier pass only when the first pass is uncertain
3. routing decision based on the classification result

Example for an expense question:

- user asks: "Can you tell me whether I can expense my lunch receipt?"
- first pass detects signals like `expense`, `lunch`, and `receipt`
- system classifies the query as `expense`
- system marks it as `rule-based`
- system routes it to policy checks rather than direct answer generation

If deterministic classification is weak, a helper AI classification step may assign routing labels from a fixed schema before policy routing continues.

## 4. Step 4 - Policy decision layer

Before retrieval or generation, the policy layer decides whether the question should be:

- answered deterministically
- answered through retrieval plus generation
- refused
- redirected

Example internal classification output:

```json
{
  "domain": "expense",
  "question_type": "rule_based",
  "sensitive": false,
  "needs_clarification": true,
  "routing_path": "policy_first"
}
```

## 5. Step 5A - Deterministic answer path

This path handles:

- lunch above 35 CHF
- alcohol expenses
- May 1 in Basel-Stadt
- sensitive IT access questions
- misconduct redirection

Examples:

- "Can I expense a 36 CHF lunch?" -> reject
- "Can I expense alcohol?" -> reject
- "What is the guest Wi-Fi password?" -> refuse in MVP
- "How do I report harassment?" -> redirect

If required fields are missing in a rule-heavy domain, the system should return a template-based clarification request instead of a free-form generated answer.

Example:

- user asks: "Can you tell me whether I can expense my lunch receipt?"
- system classifies the question as `expense`
- system detects missing decision fields
- system returns a clarification template asking for amount, person count, alcohol status, and client presence

## 6. Step 5B - Retrieval path

If the question is a supported handbook question and not blocked by policy:

- retrieve relevant chunks
- apply domain and sensitivity filters
- pass only the selected evidence onward

If multilingual support is added later, retrieval should happen after any helper translation/normalization step so the core pipeline still works on a consistent internal representation.

## 7. Step 6 - LLM generation

The LLM receives:

- the user question
- approved retrieved context
- strict prompt instructions to avoid unsupported guessing
- a structured output requirement

## 8. Step 7 - Response validation

The backend validates:

- citation presence
- citation-to-source consistency
- output schema correctness
- refusal and redirect flags

It should also validate that:

- rule-domain clarification messages came from approved template logic
- refusal and redirect messages followed the approved response strategy

## 9. Step 8 - UI response

The UI renders one of the following:

- trusted answer with citations
- refusal
- redirection

## 10. Step 9 - Audit trail

The system stores enough metadata to review:

- the query classification
- any rule triggered
- retrieved evidence
- final output type

## 11. Design Note

The system should never treat "present in source" as the only permission check for sensitive information. Sensitive access topics must be evaluated through policy, not retrieval alone.

The same principle applies to routing: the system should not rely on free-form generation to decide where a question belongs when classification can be handled through deterministic signals or a constrained classifier.

The same principle also applies to response generation: clarification, refusal, redirect, and deterministic rule messages should default to policy-controlled templates instead of free-form generation.
