# Bot Logic Flowcharts

This page documents the two decision paths for the bot:

1. **Happy Path** — the standard tool-assisted response flow.  
2. **Ombudsman Path** — the fallback path for unsupported or ambiguous cases.

---

## 1) Happy Path

### Purpose

Shows how the bot handles a query when it can use available tools and return a meaningful response.

### Flow Summary

- Send the initial system prompt and user message.  
- Call the model with the available tool definitions.  
- If the model requests a tool:  
  - Extract the tool name and arguments.  
  - Execute the tool.  
  - Append the tool result to the message history.  
  - Call the model again with the updated messages.  
- Repeat until no tool call is needed or the maximum loop rounds are reached.  
- If the model returns a valid response, return it to the user.  
- If the model returns an empty response, return a fallback message.

---

### Flowchart

```mermaid
flowchart TD

A[User Input] --> B[Send initial messages (system prompt + user message)]
B --> C[Call OpenAI with messages and tool definitions]

C --> D{Tool call?}

%% No tool call path
D -- No --> E{Response has content?}
E -- Yes --> F[Return reply to user]
E -- No --> G[Return fallback message]

%% Tool call path
D -- Yes --> H[Extract tool name and arguments]
H --> I{Which tool?}

I -- check_holiday --> J[Run check_holiday]
I -- search_handbook --> K[Run search_handbook]

J --> L[Append tool result to messages]
K --> L

L --> M[Call OpenAI again with updated messages]
M --> C

%% Loop control
C --> N{Max tool rounds reached?}
N -- Yes --> O[Return loop limit message]
---

## 2) Ombudsman Path

### Purpose

Define what happens when the bot does **not** know the answer with sufficient confidence.

### Trigger conditions

The Ombudsman Path is activated when one or more of the following happen:

- no approved evidence is found
- conflicting policy evidence is retrieved
- extraction confidence is too low
- output validation fails
- required data is missing
- system/tool failure prevents a grounded answer

### Core rule

> **No hallucination allowed.** If the bot cannot support an answer with approved evidence, it must say so clearly and safely.

### Mermaid diagram

```mermaid
flowchart TD
    A[Trigger: bot cannot answer confidently] --> B[Examples
no evidence conflicting policies low confidence validation failure]
    B --> C[1. Confidence and grounding check
Tool]
    C --> D{Can uncertainty be recovered?}
    D -- Yes --> E[2. Attempt recovery
broaden retrieval retry extraction check alternate approved sources]
    E --> F{Recovered with verified evidence?}
    F -- Yes --> G[Return to Happy path]
    F -- No --> H[3. Classify failure type
Tool]
    D -- No --> H
    H --> I[unknown_policy missing_data ambiguous_question system_error conflict_in_sources]
    I --> J[4. Generate safe response
LLM constrained by system prompt]
    J --> K[Rules
no guessing no fabricated policy explicit uncertainty cite what is known]
    K --> L{Which safe output?}
    L --> M[A. Missing policy
I could not find an approved rule for this case]
    L --> N[B. Ambiguous input
Ask for the missing detail needed to decide]
    L --> O[C. Partial grounded answer
State what is known and what is unclear]
    L --> P[D. Escalate
Route to Finance HR or human reviewer]
    M --> Q[5. Log incident for review
Tool]
    N --> Q
    O --> Q
    P --> Q
    Q --> R[Return safe uncertain response
Never hallucinate]
```

### Safe output modes

#### A. Missing policy

Use when there is no approved policy covering the case.

Example:

> I could not find an approved rule that covers this situation.

#### B. Ambiguous input

Use when the user did not provide enough information to decide safely.

Example:

> I need one more detail to answer this correctly: was an external client present?

#### C. Partial grounded answer

Use when some facts are known, but the final decision is not fully supported.

Example:

> I found the meal limit, but I could not verify whether this exception applies to your case.

#### D. Escalation

Use when the question requires human review or policy ownership.

Example:

> This case should be reviewed by Finance because I could not verify a policy exception.

---

## Design principles

### 1. The bot answers only when grounded

A confident answer requires:

- approved source evidence
- policy-consistent reasoning
- successful output validation

### 2. The LLM explains, but does not decide

The LLM is used to produce human-readable language.
It is **not** the source of truth for policy decisions.

### 3. Unknown is an allowed outcome

Saying **"I don’t know based on approved evidence"** is correct behavior.

### 4. Recovery happens before escalation

Before failing safely, the system should try:

- broader retrieval
- alternate approved sources
- constrained extraction fallback

### 5. Every uncertain case should be logged

This improves:

- policy coverage
- retrieval quality
- extraction quality
- future bot performance

---

## One-line takeaway

The bot should answer confidently only when it is grounded in approved evidence; otherwise it must clarify, provide a partial grounded response, or escalate — **never hallucinate**.
