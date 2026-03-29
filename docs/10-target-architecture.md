# Target Architecture

## GreenLeaf Logistics - Beat-Bot

## 1. Architectural Goal

Beat-Bot should behave as a trusted internal policy assistant, not as a general-purpose chatbot.

The architecture must optimize for:

- source grounding
- deterministic policy enforcement
- security-first behavior
- refusal safety
- traceability

## 2. High-Level Architecture

- `Frontend`: Next.js + TypeScript web UI
- `Backend`: FastAPI orchestration layer
- `Knowledge Base`: PostgreSQL + pgvector
- `LLM Layer`: OpenAI API
- `Policy Layer`: deterministic rules and refusal logic
- `Audit Layer`: logging and traceability

## 3. Key Architectural Principle

Policy comes before generation.

If a question can be answered deterministically or must be refused for security reasons, the system should not defer that decision to the LLM.

## 4. Main Processing Paths

### Deterministic Path

Used for:

- expense checks
- holiday checks
- sensitive-topic refusal
- misconduct redirection

### Retrieval + Generation Path

Used for:

- vacation policy questions
- handbook explanations
- office policy questions
- other supported handbook content with citations

## 4.2 Response Strategy Design

Beat-Bot should also use a hybrid response strategy.

### Template-Based Responses

Templates should be used for:

- clarification requests in rule-heavy domains
- deterministic rule outcomes
- refusal messages
- redirect messages

Examples:

- expense clarification when amount or person count is missing
- holiday clarification when date or location is missing
- refusal for Wi-Fi password requests
- redirect for harassment-related questions

### Retrieval Plus Generation Responses

Retrieval plus generation should be used for:

- handbook explanations
- policy summaries
- source-backed answers where natural-language explanation is useful

### Why This Matters

Using templates for clarification, refusal, redirect, and deterministic rule messages improves:

- consistency
- safety
- auditability
- predictability in MVP behavior

Generation should be reserved mainly for evidence-backed explanation, not for inventing control flow or policy decisions.

## 4.1 Query Classification Design

Beat-Bot should use a hybrid query-classification layer before policy routing.

### First Pass: Deterministic Classification

The first pass should use:

- keyword matching
- phrase and pattern rules
- simple heuristics

Examples:

- `expense`, `receipt`, `lunch`, `CHF`, `alcohol` -> likely `expense`
- `holiday`, `May 1`, `Basel`, `vacation day` -> likely `holiday` or `leave`
- `Wi-Fi`, `password`, `MAC`, `device registration` -> likely `IT/security`
- `harassment`, `bullying`, `whistleblowing`, `ombudsman` -> likely `sensitive conduct`

### Second Pass: Lightweight Classifier

If deterministic signals are weak or conflicting, the system may call a lightweight classifier that chooses only from a fixed label set.

The classifier should not generate answers. It should only assign routing labels such as:

- `domain`
- `question_type`
- `sensitive`
- `needs_clarification`

### Why Hybrid Classification

This project should not rely on pure keyword logic for every case, and it should not rely on full LLM judgment for every routing decision either.

Hybrid classification gives:

- speed and determinism on obvious cases
- flexibility for paraphrased questions
- lower cost and lower risk than full free-form model routing

## 5. Sensitive IT Handling Design

The architecture must explicitly support a conservative access policy.

For MVP:

- internal Wi-Fi credential requests are refused
- guest Wi-Fi password requests are refused
- MAC registration detail requests are refused
- process guidance such as "contact Sarah Muller in IT" is allowed

This means the policy layer must evaluate topic sensitivity before retrieval and generation.

## 6. Approved Data Sources

- Handbook v2.1
- Stakeholder briefing
- Holiday CSV for deterministic logic

## 7. Retrieval Design

The retrieval layer should:

- operate on section-aware chunks
- preserve metadata for section title and source
- support domain and sensitivity filtering
- keep only a small number of relevant chunks

## 8. Structured Output Contract

Trusted answers should return:

- `answer`
- `citations`
- `confidence`
- `refusal_flag`
- `policy_rule_applied`
- `redirect_target`

Classification output inside the backend may also include:

- `domain`
- `question_type`
- `sensitive`
- `needs_clarification`
- `routing_path`

## 8.1 AI-Assisted Helper Services

The architecture may use the OpenAI API not only for answer generation, but also for tightly scoped helper tasks.

These helper tasks should support the core pipeline without replacing deterministic business logic.

### Appropriate Helper Uses

- lightweight classification fallback when deterministic classification is uncertain
- translation or normalization for multilingual input
- speech-to-text transcription for future voice input

### Important Boundary

These helper uses should assist with understanding or transformation, not final policy decisions.

Examples:

- good use: classify an ambiguous user question into a fixed label set
- good use: translate a French question into the system's working language
- good use: transcribe a voice message into text
- bad use: let the model freely decide whether an expense should be reimbursed

### Architectural Rule

Use AI for `understanding and transformation`.

Use rules and policy logic for `business decisions and safety enforcement`.

## 9. Why This Architecture Fits the Problem

This design matches the problem because the project has:

- a narrow document set
- clear deterministic rules
- strict safety expectations
- strong need for proof of source

RAG alone is not enough. The project needs `RAG + deterministic policy guardrails`.

## 10. Future Extensibility

The MVP should be designed so that future input channels can be added without changing the core decision pipeline.

### Recommended Modularity Rule

Keep the core system `text-first` and `input-channel agnostic`.

That means future channels such as voice should be added as separate input adapters:

- text input adapter
- voice input adapter

The recommended future voice path is:

`Voice Input -> Speech-to-Text -> Normal Text Query Pipeline`

This allows the same core services to stay unchanged:

- query classification
- policy engine
- retrieval
- rule checks
- response generation
- response validation

### Why This Matters

This keeps post-MVP voice support modular, reduces refactoring risk, and prevents the team from coupling audio processing directly into core policy logic.
