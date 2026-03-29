# Recommended MVP Defaults

## GreenLeaf Logistics - Beat-Bot

This document proposes practical default decisions for the MVP when stakeholder clarification is still pending.

These defaults are intended to keep the scope narrow, safe, and realistic for a short delivery timeline.

These are working assumptions only. They are not final project commitments unless explicitly confirmed.

| Topic | Recommended Default |
| --- | --- |
| Login domain | Use `@powercoders.org` via Google Workspace OIDC |
| Real company domain | Do not require `@greenleaf.com` for MVP |
| User roles | Keep only `Employee` and `Admin` |
| Guest Wi-Fi password | Refuse to disclose |
| Internal Wi-Fi password | Refuse to disclose |
| MAC registration details | Refuse detailed disclosure, allow only safe IT guidance |
| IT access help | Reply with contact/process guidance like `contact Sarah Muller in IT` |
| Expense input | Start with text-based input only |
| Voice-message input | Defer until after core MVP is stable |
| Receipt upload/OCR | Defer until after core MVP is stable |
| External client verification | Rely on user declaration in MVP |
| Per-person expense rule | Ask follow-up if attendee count is missing |
| Expense clarification | Use template-based clarification messages |
| Holiday logic | Use deterministic logic from the holiday CSV |
| Sensitive conduct | Always redirect to ombudsman flow |
| General handbook answers | Use retrieval + generation with citations |
| Classification fallback | Allow a constrained AI helper step only when deterministic routing is uncertain |
| Translation support | If added later, use AI-assisted normalization before the core text pipeline |
| Transcription support | If added later, use speech-to-text before the core text pipeline |
| Refusal/redirect messages | Use templates, not free-form generation |
| Clarification messages | Use templates in rule-heavy domains |
| Logging | Keep persistent logs |
| Log contents | Store minimum necessary metadata plus rule/routing outcomes |
| Full user question storage | Allow if needed for QA, but avoid storing unnecessary sensitive details |
| Sensitive data in logs | Mask or exclude where possible |
| Log access | Admin-only |
| Log retention | Short MVP retention window, e.g. 30 days |
| Citation format | Document name + section title + page when available |
| Multi-turn support | Keep limited, only simple clarification turns |
| Auth depth | Lightweight internal auth, not production-grade enterprise IAM |
| MVP success criteria | Expense correctness, Basel holiday correctness, safe refusals, source-backed answers |

## Strongest Recommendations

- keep auth simple
- keep security strict
- keep expense and holiday logic deterministic
- keep logging minimal but persistent
- defer OCR and advanced RBAC
