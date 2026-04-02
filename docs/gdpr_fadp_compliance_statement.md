# GDPR / FADP Compliance Statement

## GreenLeaf AI Assistant ("BeatBot")
### Prepared by: Releaf Team (Powercoders Bootcamp, Bern 2026)

---

## 1. Purpose

This document explains how the GreenLeaf AI Assistant ("BeatBot") is designed to protect employee privacy in line with:

- EU General Data Protection Regulation (GDPR)  
- Swiss Federal Act on Data Protection (FADP)  

The bot is intended to answer internal policy questions based on approved company sources (e.g. handbook), including expenses, holidays, leave, IT access rules, and misconduct reporting.

The system follows a **privacy-first approach**, meaning:

- only minimal data is processed  
- unnecessary collection is avoided  
- no default long-term storage is used  

This aligns with:

- GDPR principles: data minimisation, purpose limitation, storage limitation, privacy by design/default  
- FADP principles: lawfulness, good faith, proportionality, purpose compatibility  

---

## 2. What Data the Bot Processes

### Processed Data
- User question (free-text input)  
- Minimal technical metadata (e.g. timestamp, request context)  
- Generated response and source references  

### Not Processed / Not Collected
- Name  
- Email  
- Employee ID  
- Authentication data  
- User profiles  

The system is **not designed to identify users**.

### Important Clarification

Users may include personal data in free-text input. In such cases:

- the system technically processes the text  
- but does not request, enrich, or link it to identity  

Under GDPR/FADP, *processing* includes any operation such as reading, using, or deleting data.

---

## 3. Purpose of Processing

BeatBot processes data only to:

- answer employee questions using approved sources  
- explain company policies clearly and consistently  
- enforce key business rules, including:
  - expense limit of **35 CHF per person**  
  - alcohol is **not reimbursable**  
  - Basel-Stadt holiday logic  
  - misconduct cases redirected to ombudsman  

### Not Used For
- profiling  
- employee monitoring  
- marketing  
- analytics  
- behavioral tracking  

Processing is strictly **purpose-limited and proportionate**.

---

## 4. Legal Basis

### Under GDPR

- **Art. 6(1)(f)** - Legitimate interest  
  (internal employee support)

- **Art. 6(1)(b)** - Contractual necessity (if applicable)  
  (internal tools used in employment context)

### Under Swiss FADP

Processing follows:

- lawfulness  
- good faith  
- proportionality  
- purpose limitation  
- transparency  

**Summary:**  
BeatBot processes only what is necessary to provide internal policy support.

---

## 5. Storage and Retention

### Current MVP Behavior

- Data is processed **in-memory only**  
- No persistent chat storage  

### Definitions

- **In-memory processing** = temporary data during request  
- **Long-term storage** = storing beyond request lifecycle  
- **Persistent storage** = saved in database or logs  

### Current State

- no chat history database  
- no stored Q&A records  
- `/ask` endpoint processes and returns response only  

### Optional Logging (Future)

If enabled:

- minimal data only  
- no identifiers  
- retention: **7–30 days max**  
- automatic deletion recommended  

This aligns with **storage limitation principle**.

---

## 6. Data Sharing and Disclosure

BeatBot does **not share data externally**.

### Key Distinction

The system differentiates between:

- **Allowed information**  
  (e.g. guest Wi-Fi access instructions)

- **Restricted information**  
  (e.g. internal MAC registration, security processes)

### Controls

- policy layer  
- validation before response  
- refusal logic  

---

## 7. Security and Privacy Safeguards

Implemented / Planned safeguards:

- Input validation (reject invalid requests)  
- Rule-based filtering (policy enforcement)  
- Structured responses (limit leakage risk)  

### PII Masking Layer (Planned)

The system includes a masking pipeline using:

- regex patterns  
- spaCy Named Entity Recognition  

Detects and replaces:

- emails → `[EMAIL]`  
- phone numbers → `[PHONE]`  
- names → `[PERSON]`  
- locations → `[LOCATION]`  
- IPs, URLs, IDs  

Purpose:

- reduce accidental exposure of personal data  
- enforce **data minimisation**

Note:  
Masking improves privacy but does not guarantee full compliance.  
Final compliance depends on deployment and governance.

---

## 8. Data Minimisation

Core principle:

> Only data necessary to answer the question is processed.

### Implementation

- no user tracking  
- no session persistence  
- no profile building  
- no unnecessary logs  

Aligned with:

- GDPR Art. 5(1)(c)  
- FADP proportionality principle  

---

## 9. Data Subject Rights

GDPR/FADP rights include:

- access  
- correction  
- deletion  
- restriction  
- portability  

### Practical Limitation

- system does not identify users  
- no personal dataset per user  

Therefore:

- rights are **limited in practice**

### If Logs Exist

- deletion must be supported  
- retention must be controlled  

---

## 10. International Transfers

BeatBot should be deployed in environments compliant with:

- Swiss data protection standards  
- EU GDPR requirements (if applicable)

If data is transferred outside Switzerland or EEA:

- appropriate safeguards must be applied  
- adequate protection must be ensured  

---

## 11. Conclusion

BeatBot is designed to:

- process minimal data  
- avoid long-term storage  
- enforce strict policy rules  
- prevent sensitive data exposure  
- integrate privacy controls (e.g. PII masking)

The system is **designed to align with GDPR and FADP principles**, including:

- purpose limitation  
- proportionality  
- data minimisation  
- storage limitation  
- privacy by design/default  

Final compliance depends on production setup (hosting, logging, access control).

---
