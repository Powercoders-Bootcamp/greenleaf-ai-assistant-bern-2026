# GreenLeaf AI Assistant ("Beat-Bot")

An internal AI assistant designed to automate repetitive employee questions for **GreenLeaf Logistics**, strictly adhering to company policies without hallucinations or security breaches.

---

## 👥 Team: PolicyAI Squad (Bern Group 2026)

- **Product Owner / Project Manager:** Fateme  
- **Scrum Master:** Heba  
- **AI Engineers:** Heba, Fateme  
- **Frontend Developers:** Maksat, Pema Tsering, Yasar    
- **Backend Developers:** Yurii, Yasar, Fateme, Maksat   

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
