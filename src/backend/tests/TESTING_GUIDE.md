# LLM Evaluation Testing Guide

## 1. Overview

This guide explains how to:

- Set up the environment
- Create test cases
- Run evaluation
- Analyze results

The system tests an AI assistant using predefined questions stored in CSV files.

---

## 2. Environment Setup

### Step 1: Start the system

Open terminal in the project root and run:

```bash
docker compose up -d
```

Wait until all containers are running.

Check status:
```bash
docker compose ps
```

### Step 2: Verify environment
```bash
docker compose exec backend pwd
```

## 3. Running Tests
Run all test files
```bash
docker compose exec backend python /app/src/backend/tests/eval_runner.py
```

Run a single test file
```bash
docker compose exec backend python /app/src/backend/tests/eval_runner.py --file your_file.csv
```

Example:
```bash
docker compose exec backend python /app/src/backend/tests/eval_runner.py --file test_for_test.csv
```
## 4. Test File Location

All test files must be placed in:
```bash
src/backend/tests/fixtures/
```

## 5. CSV Structure

Each test file must follow this format:
```bash
id,history,question
```
Field descriptions

id — unique identifier for the test case

history — previous conversation (JSON) or empty

question — current user input

## 6. History Field (Context Simulation)
Single-turn example:

1,,"What is the travel policy?"

Multi-turn example:

2,"[{""role"": ""user"", ""content"": ""Is it a holiday on this date?""}, {""role"": ""assistant"", ""content"": ""Please tell me the date.""}]","2026-04-13"

JSON Rules:

Must be a list

Each item must have:
role: "user" or "assistant" and
content: string

Example:

[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]
## 7. Output Files

Results are saved automatically in:

src/backend/tests/artifacts/run_YYYY-MM-DD_HH-MM-SS/

Each input file generates one output file with the same name.

Output format:

id,history,question,answer
## 8. Creating Test Cases

Generate Test Cases with ChatGPT

Use this prompt:
```bash
Generate test cases for an AI assistant.

Output format must be strictly valid CSV with the following columns:
id,history,question

General rules:
- Do NOT include any explanations, only CSV output
- The first row must be the header: id,history,question
- Each row must be a valid CSV row
- Use UTF-8 encoding
- Properly escape quotes inside CSV (double quotes "")

History field rules:
- The "history" field represents previous conversation context
- It must be either:
  1) empty (for single-turn tests)
  2) OR a valid JSON array (for multi-turn tests)

JSON structure for history:
- Must be a JSON list of message objects
- Each object must have:
  - "role": either "user" or "assistant"
  - "content": string message

Example JSON history:
[{"role":"user","content":"Is it a holiday on this date?"},{"role":"assistant","content":"Please tell me the date."}]

CSV escaping rules for JSON:
- All double quotes inside JSON must be doubled
- Entire JSON must be wrapped in quotes

Correct CSV example:
2,"[{""role"": ""user"", ""content"": ""Is it a holiday on this date?""}, {""role"": ""assistant"", ""content"": ""Please tell me the date.""}]","2026-04-13"

Test case requirements:
- Generate 10–20 test cases
- Include both:
  - Single-turn questions (empty history)
  - Multi-turn follow-up questions (with history)
- Include:
  - Normal cases
  - Edge cases (limits, boundary values)
  - Ambiguous questions
  - Clarification scenarios (assistant asks for more info, user provides it)

Topic: [INSERT TOPIC HERE]

Output only valid CSV.

```

## 9. Using Excel / Google Sheets
Step 1: Create table

Columns:

id | history | question

Step 2: Export to CSV

Excel File → Save As
Format: CSV UTF-8 (.csv)

Google Sheets
File → Download → CSV

## 10. Workflow Summary
Start Docker

Create CSV in fixtures

Run eval_runner

Open results in artifacts

Review answers

Notes:

Each row is independent

No shared memory between rows

Context must be explicitly defined in history

Results are not stored in Git (local only)
Done
