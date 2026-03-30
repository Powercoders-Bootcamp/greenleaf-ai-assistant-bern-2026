import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="GreenLeaf Assistant API")

# Налаштування CORS для підключення React-фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Моделі даних Pydantic
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

class SourceItem(BaseModel):
    title: str
    section: str
    confidence: str

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem]

@app.get("/")
def root():
    return {"status": "ok", "message": "GreenLeaf backend is running"}

@app.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    # 1. Simulate AI processing time for the UI to show the loading state
    await asyncio.sleep(1.2)
    
    # 2. Clean and uppercase the question for simple mock keyword matching
    query = payload.question.strip().upper()

    # TEST CASE 1: Security & Passwords (Beat's Rule #3)
    if "PASSWORD" in query or "WIFI" in query or "MAC" in query:
        return AskResponse(
            answer="For visitors, the guest Wi-Fi password is **GreenLeaf_2026!**. Internal network passwords or MAC address registrations must be handled directly by **Sarah Müller in IT**. Do not share internal credentials.",
            sources=[SourceItem(title="Handbook v2.1", section="6. IT, SECURITY & CONNECTIVITY", confidence="HIGH")]
        )

    # TEST CASE 2: Expenses & Alcohol (Beat's Rule #1)
    elif "LUNCH" in query or "EXPENSE" in query or "CHF" in query or "ALCOHOL" in query:
        return AskResponse(
            answer="Client lunches are only reimbursable up to **35 CHF per person**, and only if an **external client** is present. Alcohol is **strictly non-reimbursable** and must be paid on a separate personal receipt.",
            sources=[SourceItem(title="Handbook v2.1", section="7. EXPENSES & TRAVEL", confidence="HIGH")]
        )

    # TEST CASE 3: Holidays & Basel Calendar (Beat's Rule #2)
    elif "MAY 1" in query or "HOLIDAY" in query or "LABOR DAY" in query:
        return AskResponse(
            answer="We observe all national Swiss holidays. However, Labor Day (May 1st) is observed as a full holiday **ONLY for staff based in the Basel-Stadt Canton**. Staff in other regions must work.",
            sources=[
                SourceItem(title="Handbook v2.1", section="4. TIME OFF", confidence="HIGH"),
                SourceItem(title="2026 Holiday Logic (CSV)", section="Row: 01.05.2026", confidence="HIGH")
            ]
        )

    # TEST CASE 4: WORKING HOURS & SHIFTS
    elif "HOURS" in query or "START" in query or "TIME" in query or "LATE" in query:
        return AskResponse(
            answer="Standard core office hours are **08:30 to 17:30** with a mandatory **45-minute lunch break**. However, Warehouse staff in the Basel-Stadt location must be onsite by **07:00**.",
            sources=[SourceItem(title="Handbook v2.1", section="3. WORKING HOURS & ATTENDANCE", confidence="HIGH")]
        )

    # TEST CASE 5: VACATION DAYS
    elif "VACATION" in query or "DAYS OFF" in query or "ANNUAL LEAVE" in query:
        return AskResponse(
            answer="All full-time employees are entitled to **25 days** of paid annual leave. Employees over the age of 50 receive an **additional 5 days** (30 days total). Requests must be submitted **3 weeks in advance**.",
            sources=[SourceItem(title="Handbook v2.1", section="4. TIME OFF (VACATION & HOLIDAYS)", confidence="HIGH")]
        )

    # TEST CASE 6: KITCHEN / MICROWAVE (The fun operational stuff)
    elif "KITCHEN" in query or "MICROWAVE" in query or "FRIDGE" in query or "CLEAN" in query:
        return AskResponse(
            answer="Fridge items without labels will be **discarded every Friday at 16:00**. If a microwave explosion occurs, it is the **user's responsibility** to clean it immediately. Covers must be used.",
            sources=[SourceItem(title="Handbook v2.1", section="2. OFFICE ETIQUETTE & COMMUNAL SPACES", confidence="HIGH")]
        )

    # TEST CASE 7: FIRE EMERGENCY
    elif "FIRE" in query or "ALARM" in query or "EMERGENCY" in query:
        return AskResponse(
            answer="Exit via the stairwell. DO NOT use elevators. The assembly point is the **gravel parking lot** behind the main warehouse. Fire Wardens are **Thomas Bucher** (Fl. 1), **Ursula Vonolten** (Fl. 2), and **Kevin Koller** (Fl. 3).",
            sources=[SourceItem(title="Handbook v2.1", section="8. SAFETY & EMERGENCY PROCEDURES", confidence="HIGH")]
        )

    # TEST CASE 8: Bereavement / Pets (Trick Question)
    elif "DOG" in query or "PET" in query or "BEREAVEMENT" in query:
        return AskResponse(
            answer="Employees are granted 3 days of paid leave for the death of an immediate family member (spouse, child, parent), and 1 day for close relatives (grandparents, siblings). Pets are **not covered** under bereavement leave.",
            sources=[SourceItem(title="Handbook v2.1", section="5. BEREAVEMENT & SPECIAL LEAVE", confidence="HIGH")]
        )

    # DEFAULT FALLBACK: For any other questions
    return AskResponse(
        answer=f'QUERY RECEIVED: "{payload.question}". IN THE FINAL BUILD, THE AI ORCHESTRATOR WILL PARSE THE DATABASE TO GENERATE A PRECISE RESPONSE.',
        sources=[SourceItem(title="System", section="Awaiting RAG Integration", confidence="LOW")]
    )