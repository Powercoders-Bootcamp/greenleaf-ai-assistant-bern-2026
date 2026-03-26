# GreenLeaf Logistics – Beat-Bot User Stories (Refined)

## 📌 Product Vision

Deliver a reliable internal AI assistant that answers employee questions based strictly on verified company sources, reducing operational interruptions and ensuring policy compliance.

---

## 👥 User Roles

- Employee (Primary User)
- Admin (Operations / Product Owner perspective)
- IT & Security
- System

---

## 🧾 Epic 1: Expense Validation & Policy Enforcement

### User Stories

- As an Employee, I want to check if a lunch expense is reimbursable so that I avoid out-of-pocket costs.
- As an Employee, I want to understand expense limits and restrictions so that I comply with company policy.
- As an Admin, I want the assistant to strictly enforce expense policies so that financial compliance is guaranteed.
- As the System, I must reject any expense above 35 CHF so that company rules are enforced. :contentReference[oaicite:0]{index=0}
- As the System, I must reject any expense containing alcohol so that policy violations are prevented. :contentReference[oaicite:1]{index=1}
- As the System, I must only approve expenses when an external client is present so that reimbursement rules are correctly applied. :contentReference[oaicite:2]{index=2}

---

## 📅 Epic 2: Holidays & Time-Off Management

### User Stories

- As an Employee, I want to know if a specific date is a public holiday so that I can plan my work schedule.
- As an Employee based in Basel-Stadt, I want accurate regional holiday information so that I am not misinformed. :contentReference[oaicite:3]{index=3}
- As an Employee, I want to understand my annual leave entitlement so that I can plan vacations effectively. :contentReference[oaicite:4]{index=4}
- As an Employee, I want to know the vacation request process so that my requests are approved without delays.
- As an Admin, I want the assistant to differentiate between national and cantonal holidays so that location-specific accuracy is ensured.

---

## 🕒 Epic 3: Working Hours & Attendance

### User Stories

- As an Employee, I want to know the standard working hours so that I comply with company expectations. :contentReference[oaicite:5]{index=5}
- As a Warehouse Employee, I want to know my required start time so that I meet operational requirements. :contentReference[oaicite:6]{index=6}
- As an Employee, I want to understand break requirements so that I follow company policies.
- As an Admin, I want consistent answers regarding working hours so that operational clarity is maintained.

---

## 🖤 Epic 4: Special Leave & Bereavement

### User Stories

- As an Employee, I want to know how many leave days I receive for family bereavement so that I can plan accordingly. :contentReference[oaicite:7]{index=7}
- As an Employee, I want to understand approval requirements for extended leave so that I follow the correct process.
- As an Admin, I want sensitive leave policies to be communicated clearly so that employee expectations are managed appropriately.

---

## 🔐 Epic 5: IT, Security & Access Control

### User Stories

- As an Employee, I want to know how to access Wi-Fi so that I can connect to company systems.
- As an IT & Security stakeholder, I want to ensure that sensitive credentials are never exposed so that company security is maintained. :contentReference[oaicite:8]{index=8}
- As the System, I must not disclose internal Wi-Fi passwords or device registration processes to unauthorized users so that security risks are minimized. :contentReference[oaicite:9]{index=9}
- As an Employee, I want to understand password policies so that I remain compliant. :contentReference[oaicite:10]{index=10}

---

## 📚 Epic 6: Source Transparency & Trust

### User Stories

- As an Employee, I want the assistant to provide source references so that I can trust the answer.
- As an Admin, I want every response to be traceable to the handbook so that disputes can be resolved quickly. :contentReference[oaicite:11]{index=11}
- As the System, I must cite the exact source of information so that responses are verifiable.

---

## 🧠 Epic 7: Accuracy, Reliability & Risk Prevention

### User Stories

- As an Admin, I want the assistant to avoid hallucinations so that incorrect information is never communicated. :contentReference[oaicite:12]{index=12}
- As the System, I must only generate answers based on approved sources so that reliability is ensured.
- As an Employee, I want consistent and deterministic answers so that I can rely on the assistant.
- As an IT & Security stakeholder, I want safeguards against misinformation so that business risk is reduced.

---

## 💬 Epic 8: User Interaction & Experience

### User Stories

- As an Employee, I want to ask questions in natural language so that interaction is easy and intuitive.
- As an Employee, I want clear and concise responses so that I can quickly understand policies.
- As an Employee, I want the assistant to handle unclear questions safely so that I am not misinformed.
- As an Admin, I want a simple and usable interface so that adoption across teams is high.

---

## 🚫 Epic 9: Out of Scope (Non-Goals)

### User Stories

- As the System, I will not handle salary increase or compensation negotiations.
- As the System, I will not provide logistics tracking or operational warehouse data.
- As the System, I will not engage in confidential HR or misconduct discussions. :contentReference[oaicite:13]{index=13}

---

## ✅ Definition of Ready (DoR)

- User story clearly defined with role, goal, and benefit
- Acceptance criteria identified
- Dependencies and risks understood
- Prioritized in backlog

---

## ✅ Definition of Done (DoD)

- Feature implemented and tested
- Responses are accurate and source-backed
- No security violations present
- Reviewed and approved by Product Owner (Admin role)
- Ready for deployment in internal environment

---
