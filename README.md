GreenLeaf AI Assistant ("Beat-Bot")

An internal AI assistant designed for GreenLeaf Logistics to automate repetitive employee questions while strictly enforcing company policies, preventing hallucinations, and protecting sensitive data.

---

OVERVIEW

Beat-Bot is a policy-first AI system that ensures all responses are grounded in internal company rules and documentation. The assistant is designed to be predictable, secure, and resistant to misuse.

It combines retrieval-based answers with rule-based logic and explicit safety controls.

---

CORE FEATURES

- Policy-based responses with no unsupported assumptions
- Strict adherence to internal handbook content
- PII masking via a dedicated Privacy Gate
- Protection against prompt injection and misuse
- Deterministic logic for critical rules (expenses, holidays, IT policies)
- Controlled orchestration between RAG and business logic
- Optional debug mode to expose internal decision flow

---

ARCHITECTURE

The system follows a Policy-First RAG architecture:

1. User input is received
2. Privacy Gate processes and masks sensitive data
3. Orchestrator determines the correct path:
   - Retrieve information from internal documents (RAG)
   - Apply strict business logic rules
   - Reject unsafe or out-of-scope requests
4. The assistant returns a validated, policy-compliant response

Example enforced rules:

- Expenses above 35 CHF are rejected
- Alcohol-related expenses are not allowed
- Basel holidays are handled via strict logic
- Sensitive IT-related data is blocked

---

TECH STACK

Frontend:
- React (Vite)
- TypeScript
- CSS

Backend:
- FastAPI (Python)
- Uvicorn
- OpenAI API

AI / Data:
- Retrieval-Augmented Generation (RAG)
- Custom orchestration layer
- Rule-based validation system

Tooling:
- Git & GitHub
- Postman (API testing)

---

PROJECT STRUCTURE

data/
  raw/                # raw input documents
  processed/          # processed data for RAG

db/
  logging_schema.sql  # database schema for logging

docs/
  adr/                # architectural decisions
  diagrams/           # system diagrams
  archive/            # archived docs
  *.md                # architecture, QA, requirements, etc.

prompts/
  system_prompt.txt   # system instructions
  tools_definitions/  # tool configs

src/
  backend/
    api/              # API routes
    core/             # core logic
    services/         # orchestration & logic
    models/           # data models
    schemas/          # validation schemas
    tests/            # backend tests
    main.py           # entry point
    pii_masker.py     # privacy gate
  frontend/
    src/              # React application
    public/           # static assets

docker-compose.yml     # container orchestration
Docker_manual.md       # docker instructions

---

RUNNING THE PROJECT LOCALLY

Backend:

See detailed setup in:
src/backend/README.md

Run:

cd src
.\backend\myenv\Scripts\Activate
uvicorn backend.main:app --reload --port 8000

Backend:
http://127.0.0.1:8000

API Docs:
http://127.0.0.1:8000/docs

---

Frontend:

cd src/frontend
npm install
npm run dev

Frontend:
http://localhost:5173

---

DOCUMENTATION

The docs folder contains:

- Strategy: product vision and scope
- Architecture: system design and flow
- QA: testing approach
- ADR: architectural decisions
- Security: access control and compliance

---

DEVELOPMENT STATUS

- Backend API implemented (FastAPI)
- Frontend chat interface completed
- End-to-end communication established
- Error and loading handling implemented
- Core policy enforcement in place
- Privacy Gate implemented
- Basic red-team protections added

---

TEAM

Bern Group 2026

- Product Owner / Project Manager: Fateme
- Scrum Master: Heba
- AI Engineers: Heba, Fateme
- Frontend Developers:  Pema Tsering, Yasar, Maksat
- Backend Developers: Yurii, Yasar, Fateme, Maksat

---

MISSION

To build a reliable internal AI assistant that delivers accurate, policy-compliant answers, reduces repetitive workload, and ensures safe usage of AI within the company.

---

Powercoders Bootcamp (Bern 2026)
