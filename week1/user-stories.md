# User Stories - BeatBot (First 10)

## Format

All user stories follow:

As a [role], I want [goal], so that [benefit]
---

## 1. Redirect Sensitive Conduct Issues (#20)

**Description**  
As an Employee, I want misconduct-related questions redirected safely so that I use the correct process.

**Acceptance Criteria**
- Harassment/bullying queries are detected  
- No direct answers are given  
- User is redirected to ombudsman contact  

---

## 2. Improve Answer Readability (#24)

**Description**  
As an Employee, I want clear answer formatting so that the response is easy to scan.

**Acceptance Criteria**
- Responses are structured (bullet points or short paragraphs)  
- Key information is easy to identify  
- Answers are concise, professional, short and readable  

---

## 3. Ensure Consistent Responses (#25)

**Description**  
As an Admin, I want consistent answers so that employees receive reliable guidance.

**Acceptance Criteria**
- Similar questions produce similar answers  
- Tone is consistent across responses  
- No contradictory answers are generated  

---

## 4. Implement Logging for Q&A (#26)

**Description**  
As a Developer, I want logs for questions and responses so that I can debug and evaluate behavior.

**Acceptance Criteria**
- User questions are logged  
- System responses are logged  
- Errors are recorded for debugging  

---

## 5. Add Basic System Monitoring (#27)

**Description**  
As an Admin, I want basic visibility into system behavior so that I can review reliability.

**Acceptance Criteria**
- Admin can access logs or metrics  
- System usage is visible  
- Basic monitoring exists  

---

## 6. Answer Vacation and Leave Questions (#28)

**Description**  
As an Employee, I want to ask about vacation and leave policies so that I understand my entitlements.

**Acceptance Criteria**
- System explains 25 days annual leave  
- Senior bonus (age 50+) is included  
- Request process (3 weeks + HR portal) is explained  
- Bereavement leave rules are handled correctly  

---

## 7. Provide Working Hours Information (#29)

**Description**  
As an Employee, I want to know working hours so that I can plan my schedule.

**Acceptance Criteria**
- Core hours (08:30–17:30) are provided  
- Lunch break (45 min) is included  
- Special cases (warehouse 07:00) are handled  

---

## 8. Answer Office Policy Questions (#30)

**Description**  
As an Employee, I want to ask about office rules so that I follow company guidelines.

**Acceptance Criteria**
- Kitchen rules are answered correctly  
- Fridge labeling policy is explained  
- Cleaning responsibilities are described  

---

## 9. Log User Questions with Identity (#35)

**Description**  
As an Admin, I want to see who asked which question so that I can monitor system usage and accuracy.

**Acceptance Criteria**
Each question is stored with:
- User name  
- Company ID  
- Question text  
- System response  

Additional:
- Data is accessible for review  
- Logs are stored securely  

---

## 10. Request Clarification for Unclear Questions (#36)

**Description**  
As an Employee, I want the system to ask for more details when my question is unclear so that I get a correct answer.

**Acceptance Criteria**
- System detects unclear or incomplete questions  
- System asks a follow-up question instead of guessing  
- System refuses to answer if insufficient information is provided  

---

---

## 11. Build Document Ingestion Pipeline (#22)

**Description**  
As the System, I want approved documents ingested into a searchable store so that the assistant can retrieve evidence.

**Acceptance Criteria**
- Handbook is parsed and chunked  
- CSV holiday data is loaded  
- Metadata stored for retrieval  
- Data is searchable  

---

## 12. User Authentication & Role Awareness (#37)

**Description**  
As the System, I want users to be authenticated and roles identified so that responses respect permissions and admin functions.

**Acceptance Criteria**
- User login via company ID  
- Role assigned (Employee vs Admin)  
- Access to admin features only for Admins  

---

## 13. Extract Key Rules from Handbook (#2)

**Description**  
As the System, I want to extract key rules from the handbook so that policies can be structured and used for answering.

**Acceptance Criteria**
- Key rules are identified and extracted  
- Policies are structured into usable format  
- Content is ready for retrieval  

---

## 14. Define Expense Validation Logic (#3)

**Description**  
As the System, I want to define expense validation rules so that reimbursement decisions are consistent and policy-based.

**Acceptance Criteria**
- Expense limits are clearly defined  
- Validation rules follow company policy  
- System can evaluate if expense is allowed or rejected  

---

## 15. Define Holiday Logic (Basel vs Others) (#4)

**Description**  
As the System, I want to define holiday logic based on Basel-Stadt so that responses are accurate for the correct region.

**Acceptance Criteria**
- Basel-Stadt calendar is used as primary source  
- Differences with other regions are handled  
- Holidays are correctly returned per query  

---

## 16. Define Assistant Boundaries (Forbidden Topics) (#5)

**Description**  
As the System, I want to define forbidden topics so that sensitive or restricted information is not disclosed.

**Acceptance Criteria**
- Restricted topics are clearly defined  
- System refuses forbidden requests  
- Safe fallback response is provided  

---

## 17. Frontend UX (#38)

**Description**  
As an Employee, I want a polished, professional interface so that the bot feels reliable and aligned with the company.

**Acceptance Criteria**
- Answers formatted clearly  
- Color palette follows company guidelines  
- Response style is short, professional, easy to read  

---

## 18. Implement Question Input Interface (#13)

**Description**  
As an Employee, I want to ask a policy question in natural language so that I can get an answer quickly.

**Acceptance Criteria**
- User can input a question via UI or API  
- Input supports free text (natural language)  
- Request is sent to backend successfully  
- Errors are handled (empty input, invalid format)  

---

## 19. Enforce Grounded Responses (No Hallucinations) (#14)

**Description**  
As an Employee, I want trusted answers from the handbook so that I can rely on the assistant.

**Acceptance Criteria**
- Answers are generated only from approved sources  
- System refuses to answer when confidence is low  
- The system does not invent policy details  

---

## 20. Implement Retrieval Before Answering (#23)

**Description**  
As the System, I must retrieve relevant content before answering so that the answer is grounded.

**Acceptance Criteria**
- Relevant chunks are retrieved per query  
- Irrelevant data is minimized  
- Retrieved content is usable for citation  

---

---

## 21. Add Source Citation to Responses (#15)

**Description**  
As an Employee, I want to see the source of an answer so that I can verify it myself.

**Acceptance Criteria**
- Each response includes a citation  
- Citation references handbook section or CSV  
- Citation is human-readable (not raw data)  

---

## 22. Handle Unknown Questions Safely (#31)

**Description**  
As an Employee, I want clear feedback when the system cannot answer so that I know what to do next.

**Acceptance Criteria**
- System clearly states it cannot answer  
- No guessing or hallucination  
- Safe fallback message is provided  

---

## 23. Implement Basel-Stadt Holiday Handling (#18)

**Description**  
As an Employee, I want correct holiday answers for Basel-Stadt so that I can plan my work.

**Acceptance Criteria**
- May 1 is recognized as a holiday in Basel-Stadt  
- National vs cantonal holidays are distinguished  
- Basel-Stadt is used as default location  

---

## 24. Enforce 35 CHF Expense Rule (#16)

**Description**  
As the System, I must reject expenses above 35 CHF per person so that company policy is enforced.

**Acceptance Criteria**
- Expenses > 35 CHF are rejected  
- Exactly 35 CHF is allowed  
- Response explains the rule clearly  

---

## 25. Detect and Reject Alcohol Expenses (#17)

**Description**  
As the System, I must reject alcohol-related expenses so that company policy is enforced.

**Acceptance Criteria**
- Alcohol-related keywords are detected  
- Requests involving alcohol are rejected  
- Response explains policy clearly  

---

## 26. Handle Wi-Fi and IT-related Questions Securely (#19)

**Description**  
As the System, I must handle IT-related questions safely so that sensitive information is protected.

**Acceptance Criteria**
- Internal Wi-Fi credentials are never shared  
- Guest Wi-Fi can be provided  
- MAC registration details are restricted  
- Response clearly separates allowed vs restricted info  

---

## 27. Create Backend /ask Endpoint (#21)

**Description**  
As a Developer, I want a working /ask endpoint so that the frontend can communicate with the backend.

**Acceptance Criteria**
- Endpoint accepts POST requests  
- Request/response schema is defined  
- Invalid input is handled safely  
- Returns structured response  

---

## 28. Define Project Scope (MoSCoW) (#1)

**Description**  
Define what the product will and will not do based on stakeholder needs, and identify risks early.

**Acceptance Criteria**
- MoSCoW prioritization (Must, Should, Could, Won’t) is completed  
- Scope boundaries are clearly documented  
- Included and excluded topics are defined  
- At least one key risk is identified  

---

## 29. Create Team Charter and Define Team Structure (#34)

**Description**  
Set up the team foundation by defining roles, team identity, and working principles.

**Acceptance Criteria**
- Roles are clearly assigned (Scrum Master, PO, Devs, QA, AI Engineer)  
- Team name is defined  
- Mission and purpose are clearly written  
- Values and principles are documented  
- Ground rules are defined  
- Definition of Done is agreed  

---