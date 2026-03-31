# GreenLeaf AI Assistant ("Beat-Bot")

An internal AI assistant designed to automate repetitive employee questions for **GreenLeaf Logistics**, strictly adhering to company policies without hallucinations or security breaches.

---

## 👥 Team: Bern Group 2026

- **Product Owner / Project Manager:** Fateme  
- **Scrum Master:** Heba  
- **AI Engineers:** Heba, Fateme  
- **Frontend Developers:** Maksat, Pema Tsering, Yasar    
- **Backend Developers:** Yurii, Yasar, Fateme, Maksat   

## 🤝 Team Charter

### 🎯 Mission
Our mission is to build a reliable internal AI assistant for GreenLeaf Logistics that provides accurate, policy-based answers, reduces repetitive employee questions, and ensures compliance with company rules.

---

### 💡 Values
- **Transparency** – We communicate openly about progress, issues, and blockers  
- **Ownership** – Everyone takes responsibility for their tasks and outcomes  
- **Collaboration** – We support each other and share knowledge  
- **Pragmatism** – We focus on simple, working solutions over perfection  

---

### ⚙️ Ground Rules

**Decision Making**
- We aim for team consensus  
- If no agreement is reached, the Product Owner makes the final decision  

**Communication**
- Main communication via Slack  
- Important decisions are documented in GitHub  
- Team members respond within a reasonable time (max 24h on working days)

**Handling Issues / Conflicts**
- Issues are raised early and discussed openly  
- We focus on solutions, not blame  
- If needed, we escalate within the team  

---

### ✅ Definition of Done

A task is considered “done” when:
- The feature works as expected  
- Code is pushed and integrated into the future branch
- No critical errors are present  
- The functionality is tested manually  
- The task is clearly understandable for the team
- No major bugs or blockers remain

---

## 🚀 How to Run Locally

### Backend (FastAPI)

cd src/backend  
.\.venv\Scripts\Activate  
uvicorn main:app --reload --port 8000  

Backend: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs  

---

### Frontend (React + Vite)

cd src/frontend  
npm install  
npm run dev  

Frontend: http://localhost:5173  

---

## 🏗️ Architecture

Policy-First RAG Architecture (Modular Monolith)

Rules:
- Expenses > 35 CHF → rejected  
- Alcohol → rejected  
- Basel holidays → strict logic  
- Sensitive IT data → blocked  

---

## 📚 Docs

/docs folder contains:
- Strategy
- Architecture
- QA

---

## ✅ Sprint 1

- FastAPI /ask endpoint  
- React UI  
- End-to-end flow  
- Loading & error handling  

---

## 🧠 Stack

Frontend: React + Vite  
Backend: FastAPI  

---

Built during Powercoders Bootcamp (Bern 2026)
