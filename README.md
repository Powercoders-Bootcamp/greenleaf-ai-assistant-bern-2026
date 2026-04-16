# GreenLeaf AI Assistant ("Beat-Bot")

An internal AI assistant designed for **GreenLeaf Logistics** to automate repetitive employee questions while strictly enforcing company policies, preventing hallucinations, and protecting sensitive data.

---

## Overview

Beat-Bot is a policy-first AI system that ensures all responses are grounded in internal company rules and documentation. The assistant is designed to be predictable, secure, and resistant to misuse.

It combines retrieval-based answers with rule-based logic and explicit safety controls.

---

## Core Features

- Policy-based responses with no unsupported assumptions
- Strict adherence to internal handbook content
- PII masking via a dedicated Privacy Gate
- Protection against prompt injection and misuse
- Deterministic logic for critical rules (expenses, holidays, IT policies)
- Controlled orchestration between RAG and business logic
- Optional debug mode to expose internal decision flow

---

## Architecture

The system follows a **Policy-First RAG architecture**:

1. User input is received
2. Privacy Gate processes and masks sensitive data
3. Orchestrator determines the correct path:
   - Retrieve information from internal documents (RAG)
   - Apply strict business logic rules
   - Reject unsafe or out-of-scope requests
4. The assistant returns a validated, policy-compliant response

### Example enforced rules

- Expenses above 35 CHF are rejected
- Alcohol-related expenses are not allowed
- Basel holidays are handled via strict logic
- Sensitive IT-related data is blocked

---

## Tech Stack

### Frontend
- React (Vite)
- TypeScript
- CSS

### Backend
- FastAPI (Python)
- Uvicorn
- OpenAI API

### AI / Data
- Retrieval-Augmented Generation (RAG)
- Custom orchestration layer
- Rule-based validation system

### Tooling
- Git & GitHub
- Postman (API testing)

---

## Project Structure

**    src/
    ├── frontend/ # React user interface
    ├── backend/ # FastAPI application
    ├── docs/ # Project documentation (strategy, architecture, QA)**

---

## Running the Project Locally

### Backend

For full setup instructions (virtual environment, dependencies, environment variables), see:

src/backend/README.md

Run the backend:
    **cd src
    .\backend\myenv\Scripts\Activate
    uvicorn backend.main:app --reload --port 8000**

Backend:
**  http://127.0.0.1:8000
**
API Docs:
**  http://127.0.0.1:8000/docs
**
---

### Frontend
  cd src/frontend
  npm install
  npm run dev


  Frontend:
      http://localhost:5173

---

## Documentation

The `/docs` folder contains supporting project materials:

- Strategy – product vision, scope, and use cases  
- Architecture – system design and data flow  
- QA – testing approach and validation strategy  

---

## Development Status

- Backend API implemented (FastAPI)
- Frontend chat interface completed
- End-to-end communication established
- Error and loading handling implemented
- Core policy enforcement in place

---

## Team

Bern Group 2026

- Product Owner / Project Manager: Fateme  
- Scrum Master: Heba  
- AI Engineers: Heba, Fateme  
- Frontend Developers: Maksat, Pema Tsering, Yasar  
- Backend Developers: Yurii, Yasar, Fateme, Maksat  

---

## Mission

To build a reliable internal AI assistant that delivers accurate, policy-compliant answers, reduces repetitive workload, and ensures safe usage of AI within the company.

---

Built during Powercoders Bootcamp (Bern 2026)
