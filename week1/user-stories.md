# User Stories Backlog

## 1- Frontend UX

**Description:**  
As an Employee, I want a polished, professional interface so that the bot feels reliable and aligned with the company.

**Acceptance Criteria:**  
- Answers formatted clearly
- Color palette follows company guidelines
- Response style is short, professional, easy to read

---

## 2- Implement question input interface

Natural Language Question Input:

**Description:**  
As an Employee, I want to ask a policy question in natural language so that I can get an answer quickly.

**Acceptance Criteria:**  
- User can input a question via UI or API
- Input supports free text (natural language)
- Request is sent to backend successfully
- Errors are handled (empty input, invalid format)

---

## 3- Enforce grounded responses (no hallucinations)

Trusted Answers Only:

**Description:**  
As an Employee, I want trusted answers from the handbook so that I can rely on the assistant.

**Acceptance Criteria:**  
- Answers are generated only from approved sources
- System refuses to answer when confidence is low
- The system does not invent policy details

---

## 4- Implement retrieval before answering

Retrieval Mechanism:

**Description:**  
As the System, I must retrieve relevant content before answering so that the answer is grounded.

**Acceptance Criteria:**  
- Relevant chunks are retrieved per query
- Irrelevant data is minimized
- Retrieved content is usable for citation

---

## 5- Build document ingestion pipeline

Document Ingestion:

**Description:**  
As the System, I want approved documents ingested into a searchable store so that the assistant can retrieve evidence.

**Acceptance Criteria:**  
- Handbook is parsed and chunked
- CSV holiday data is loaded
- Metadata stored for retrieval
- Data is searchable

---

## 6- Add source citation to responses

Source Citation:

**Description:**  
As an Employee, I want to see the source of an answer so that I can verify it myself.

**Acceptance Criteria:**  
- Each response includes a citation
- Citation references handbook section or CSV
- Citation is human-readable (not raw data)

---

## 7- Handle unknown questions safely

Safe Fallback Response

**Description:**  
As an Employee, I want clear feedback when the system cannot answer so that I know what to do next.

**Acceptance Criteria:**  
- System clearly says it cannot answer
- No guessing or hallucination

---

## 8- Implement Basel-Stadt holiday handling

Basel Holiday Logic:

**Description:**  
As an Employee, I want correct holiday answers for Basel-Stadt so that I can plan my work.

**Acceptance Criteria:**  
- May 1 is recognized as a holiday in Basel-Stadt
- National vs cantonal holidays are distinguished
- The system always assumes Basel-Stadt as the default location

---

## 9- Enforce 35 CHF expense rule

Expense Limit Validation:

**Description:**  
As the System, I must reject expenses above 35 CHF per person so that company policy is enforced.

**Acceptance Criteria:**  
- Expenses > 35 CHF are rejected
- Response clearly explains the rule
- Edge cases handled (exactly 35 CHF = allowed)

---

## 10- Detect and reject alcohol expenses

Alcohol Expense Rejection:

**Description:**  
As the System, I must reject alcohol expenses so that company policy is enforced.

**Acceptance Criteria:**  
- Alcohol-related keywords are detected
- Requests involving alcohol are rejected
- Response explains policy clearly

---

## 11- Handle Wi-Fi and IT-related questions securely

Sensitive IT Protection:

**Description:**  
As the System, I must handle IT-related questions safely so that sensitive information is protected while allowing approved access.

**Acceptance Criteria:**  
- Internal Wi-Fi credentials are refused
- Guest Wi-Fi password can be shared
- MAC registration details are refused
- The response clearly distinguishes between allowed and restricted information

---

## 12- Create backend /ask endpoint

**Description:**  
As a Developer, I want a working /ask endpoint so that the frontend can communicate with the backend.

**Acceptance Criteria:**  
- Endpoint accepts POST requests
- Request/response schema defined
- Handles invalid input safely
- Returns structured response

---

## 13- Redirect sensitive conduct issues

Misconduct Handling Redirect:

**Description:**  
As an Employee, I want misconduct-related questions redirected safely so that I use the correct process.

**Acceptance Criteria:**  
- Harassment/bullying queries are detected
- No direct answers are given
- User is redirected to ombudsman contact

---

## 14- Improve answer readability

Response Formatting:

**Description:**  
As an Employee, I want clear answer formatting so that the response is easy to scan.

**Acceptance Criteria:**  
- Responses are structured (bullet points or short paragraphs)
- Key information is easy to identify
- Answers are concise, professional, short and readable

---

## 15- Ensure consistent responses

Answer Consistency:

**Description:**  
As an Admin, I want consistent answers so that employees receive reliable guidance.

**Acceptance Criteria:**  
- Similar questions produce similar answers
- Tone is consistent across responses
- No contradictory answers are generated

---

## 16- Implement logging for Q&A

Logging System:

**Description:**  
As a Developer, I want logs for questions and responses so that I can debug and evaluate behavior.

**Acceptance Criteria:**  
- User questions are logged
- System responses are logged
- Errors are recorded for debugging

---

## 17- Add basic system monitoring

Admin Visibility:

**Description:**  
As an Admin, I want basic visibility into system behavior so that I can review reliability.

**Acceptance Criteria:**  
- Admin can access logs or metrics
- System usage is visible
- Basic monitoring exists

---

## 18- Answer vacation and leave questions

**Description:**  
As an Employee, I want to ask about vacation and leave policies so that I understand my entitlements.

**Acceptance Criteria:**  
- System explains 25 days annual leave
- Senior bonus (age 50+) is included
- Request process (3 weeks + HR portal) is explained
- Bereavement leave rules are handled correctly

---

## 19- Provide working hours information

Working Hours Information:

**Description:**  
As an Employee, I want to know working hours so that I can plan my schedule.

**Acceptance Criteria:**  
- Core hours (08:30–17:30) are provided
- Lunch break (45 min) is included
- Special cases (warehouse 07:00) are handled

---

## 20- Answer office policy questions

Office Policy Questions:

**Description:**  
As an Employee, I want to ask about office rules so that I follow company guidelines.

**Acceptance Criteria:**  
- Kitchen rules are answered correctly
- Fridge labeling policy is explained
- Cleaning responsibilities are described

---

## 21- Log user questions with identity

Log user questions with identity

**Description:**  
As an Admin, I want to see who asked which question so that I can monitor system usage and accuracy.

**Acceptance Criteria:**  
- Each question is stored with:
- User name
- Company ID
- Question text
- System response
- Data is accessible for review
- Logs are stored securely

---

## 22- Request clarification for unclear questions

Clarification When Unsure

**Description:**  
As an Employee, I want the system to ask for more details when my question is unclear so that I get a correct answer.

**Acceptance Criteria:**  
- System detects unclear or incomplete questions
- If the question is unclear, system asks a follow-up question requiring more info from user instead of guessing
- System refuses to answer if insufficient information is provided

---

## 23- User Authentication & Role Awareness

User Authentication & Role Awareness

**Description:**  
As the System, I want users to be authenticated and roles identified so that responses respect permissions and admin functions.

**Acceptance Criteria:**  
- User login via company ID
- Role assigned (Employee vs Admin)
- Access to admin features only for Admins

---