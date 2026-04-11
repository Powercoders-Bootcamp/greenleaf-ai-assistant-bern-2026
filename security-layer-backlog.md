# Technical Backlog

## Beat-Bot Security Layer

## 1. Purpose

This document turns the revised security roadmap into an implementation-first technical backlog.

It assumes the target authentication model is:

- JWT/OIDC-based real user login

It is intentionally ordered so the security layer is built from the core architecture outward:

1. identity
2. authorization
3. persistence model
4. auth flow
5. protected routes
6. LLM safety and privacy
7. operational hardening

This is the order that should be followed.

## 2. Target Architecture Assumptions

The backlog assumes:

- users authenticate through an OIDC provider
- the frontend obtains an identity token or access token
- the backend validates JWTs
- the backend resolves an application user
- the backend maps users to internal roles
- the backend enforces route and data access rules server-side

Initial roles:

- `Employee`
- `Admin`

Optional later:

- `Service`

## 3. Delivery Order

| Epic | Priority | Outcome |
|------|------|------|
| BL-01 | Critical | Identity and role model defined |
| BL-02 | Critical | Authorization matrix defined |
| BL-03 | Critical | Security-aware database model created |
| BL-04 | Critical | JWT/OIDC authentication flow implemented |
| BL-05 | Critical | Current user resolution and role mapping implemented |
| BL-06 | Critical | Ownership-based route protection implemented |
| BL-07 | High | Admin-only routes and review access implemented |
| BL-08 | High | Chat persistence aligned with privacy rules |
| BL-09 | High | LLM privacy and disclosure enforcement designed and implemented |
| BL-10 | Medium | Abuse protection, observability, and operational hardening refined |

## 4. Epic BL-01 - Define Identity And Role Model

### Goal

Create an explicit identity model before implementing more security code.

### Tasks

#### BL-01.1 Define identity sources

Decide and document:

- which OIDC provider is used
- whether the frontend sends ID token or access token
- whether the backend validates JWT directly or via provider metadata/JWKS
- which claims are trusted

Output:

- short architecture note

Acceptance criteria:

- trusted claims are explicitly listed
- token issuer and audience rules are defined

#### BL-01.2 Define internal roles

Define:

- `Employee`
- `Admin`

For each role specify:

- business meaning
- allowed route categories
- allowed data visibility

Output:

- role definition table

Acceptance criteria:

- roles are understandable without reading code
- admin powers are explicit, not implied

#### BL-01.3 Define auth context contract

Design the backend auth context object that every protected route will use.

Suggested fields:

- `user_id`
- `email`
- `role`
- `auth_method`
- `token_subject`
- `provider`

Output:

- `AuthContext` design

Acceptance criteria:

- the contract can support all protected routes
- the contract does not depend on transport-specific details

Dependencies:

- none

## 5. Epic BL-02 - Define Authorization Matrix

### Goal

Define exactly what each role can do before implementing endpoints.

### Tasks

#### BL-02.1 Create route access matrix

Define allowed roles for:

- `POST /chat`
- `GET /me`
- `GET /history`
- `GET /history/{chat_id}`
- `GET /admin/chats`
- `GET /admin/users`
- `GET /health`

Output:

- route-to-role matrix

Acceptance criteria:

- every route has an explicit allowed-role list

#### BL-02.2 Define ownership rules

Define:

- who owns a chat
- who owns a message
- whether admins can read all chats or only metadata
- whether admins can read raw text or only masked text

Output:

- ownership rules section

Acceptance criteria:

- employee access is owner-based
- admin access is explicit and auditable

#### BL-02.3 Define denial behavior

Decide standard responses for:

- unauthenticated access
- authenticated but forbidden access
- resource exists but belongs to another user

Recommended:

- `401` for unauthenticated
- `403` for forbidden

Output:

- security response conventions

Dependencies:

- BL-01

## 6. Epic BL-03 - Add Security-Aware Database Model

### Goal

Create the persistence model that identity and authorization require.

### Tasks

#### BL-03.1 Add user model

Create a `users` table or ORM model.

Suggested fields:

- `id`
- `email`
- `display_name`
- `role`
- `oidc_subject`
- `issuer`
- `is_active`
- `created_at`
- `updated_at`

Output:

- user model
- migration

Acceptance criteria:

- user can be uniquely resolved from OIDC identity

#### BL-03.2 Add chat model

Create a `chats` table or ORM model.

Suggested fields:

- `id`
- `user_id`
- `title`
- `created_at`
- `updated_at`

Acceptance criteria:

- ownership can be enforced from `user_id`

#### BL-03.3 Add message model

Create a `messages` table or ORM model.

Suggested fields:

- `id`
- `chat_id`
- `sender_type`
- `content_masked`
- optional `content_raw_encrypted`
- `created_at`

Important:

- decide whether raw content is stored at all
- default recommendation is masked-only storage unless there is a strong reason otherwise

Acceptance criteria:

- privacy policy is reflected in schema

#### BL-03.4 Add audit event model if needed

Optional, but recommended if admin review or compliance matters.

Suggested fields:

- `id`
- `actor_user_id`
- `event_type`
- `resource_type`
- `resource_id`
- `metadata_json`
- `created_at`

Dependencies:

- BL-01
- BL-02

## 7. Epic BL-04 - Implement JWT/OIDC Authentication

### Goal

Replace shared-token thinking with real user authentication.

### Tasks

#### BL-04.1 Add provider configuration

Add environment settings for:

- `OIDC_ISSUER`
- `OIDC_AUDIENCE`
- `OIDC_JWKS_URL`
- optional provider name

Output:

- config support

Acceptance criteria:

- backend can start with provider config

#### BL-04.2 Implement JWT validation module

Create a dedicated auth validator module.

Responsibilities:

- read bearer token
- validate signature
- validate issuer
- validate audience
- validate expiry
- parse trusted claims

Output:

- JWT validation service

Acceptance criteria:

- invalid token fails
- expired token fails
- wrong issuer fails
- wrong audience fails

#### BL-04.3 Build OIDC identity extraction

Resolve trusted claims such as:

- `sub`
- `email`
- `name`

Output:

- normalized identity object

Acceptance criteria:

- identity extraction is independent from route logic

Dependencies:

- BL-01
- BL-03

## 8. Epic BL-05 - Resolve Current User And Role Mapping

### Goal

Translate external identity into an internal application user and role.

### Tasks

#### BL-05.1 Add user lookup/upsert flow

On authenticated request:

- find user by `oidc_subject` and `issuer`
- create user on first login if policy allows
- otherwise reject unknown user

Output:

- user resolution service

Acceptance criteria:

- authenticated request maps to a stable internal `user_id`

#### BL-05.2 Add role mapping rules

Decide how role is assigned:

- stored in DB
- seeded manually
- assigned from trusted group claim

Recommended:

- role stored in application DB

Acceptance criteria:

- role can change without changing code

#### BL-05.3 Implement `get_current_user`

Create a route dependency that returns a complete `AuthContext`.

Output:

- dependency for protected routes

Acceptance criteria:

- routes no longer depend on static role assumptions

Dependencies:

- BL-03
- BL-04

## 9. Epic BL-06 - Implement Ownership-Based Route Protection

### Goal

Protect user resources with actual ownership logic.

### Tasks

#### BL-06.1 Add `GET /me`

Return current authenticated user profile and role.

Acceptance criteria:

- authenticated users can resolve their own identity

#### BL-06.2 Add `GET /history`

Return only the current user's chats.

Acceptance criteria:

- employee cannot read another user's history

#### BL-06.3 Add `GET /history/{chat_id}`

Return one chat only if:

- current user owns it
- or current user is admin and policy allows access

Acceptance criteria:

- wrong-owner access is blocked with `403`

#### BL-06.4 Add reusable ownership guard

Implement helper such as:

- `ensure_chat_owner_or_admin`

Output:

- reusable ownership dependency/service

Dependencies:

- BL-02
- BL-05

## 10. Epic BL-07 - Implement Admin-Protected Access

### Goal

Add explicit admin-only capabilities after base ownership is working.

### Tasks

#### BL-07.1 Add admin role dependency

Implement:

- `require_admin`

Acceptance criteria:

- non-admin users receive `403`

#### BL-07.2 Add `GET /admin/chats`

Define exactly what this returns:

- all chats
- limited metadata
- filtered review list

Recommendation:

- start with minimal metadata view unless raw text access is required

Acceptance criteria:

- route is admin-only
- response scope matches policy

#### BL-07.3 Add admin access audit logging

Whenever admin accesses privileged data, emit an auditable event.

Acceptance criteria:

- privileged access is observable

Dependencies:

- BL-02
- BL-05
- BL-06

## 11. Epic BL-08 - Align Chat Processing With Privacy Rules

### Goal

Ensure persistence and processing match privacy policy.

### Tasks

#### BL-08.1 Decide storage policy

Choose one:

1. store masked text only
2. store raw text encrypted plus masked text
3. store no text history

Recommended default:

- masked text only

Acceptance criteria:

- the choice is documented and implemented consistently

#### BL-08.2 Align chat write path

Make sure chat creation and message persistence follow the chosen policy.

Acceptance criteria:

- stored fields match privacy decision

#### BL-08.3 Review PII masking position

Confirm where masking happens:

- before upstream LLM call
- before persistence
- both

Acceptance criteria:

- masking behavior is deterministic and documented

Dependencies:

- BL-03

## 12. Epic BL-09 - Design And Implement LLM Policy Enforcement

### Goal

Add server-side policy enforcement for sensitive disclosures.

### Important Constraint

Do not rely only on the system prompt.

Do not start with simplistic keyword blocking as the final design.

### Tasks

#### BL-09.1 Define restricted disclosure categories

Examples:

- internal credentials
- sensitive internal technical details
- protected HR process boundaries
- restricted identifiers

Output:

- policy category list

#### BL-09.2 Define enforcement points

Decide where policy is enforced:

- input stage
- retrieval stage
- generated draft validation stage
- response release stage

Recommendation:

- validate generated output before final release

#### BL-09.3 Implement policy validation layer

Add a dedicated validation component that can:

- inspect candidate response
- classify against policy categories
- block or rewrite unsafe output
- return safe fallback guidance

Acceptance criteria:

- restricted topics are blocked or redirected by backend policy
- allowed questions still pass

Dependencies:

- BL-02
- BL-08

## 13. Epic BL-10 - Refine Hardening And Operations

### Goal

Finish the supporting layers after core security behavior is correct.

### Tasks

#### BL-10.1 Improve abuse protection

Refine:

- rate limiting strategy
- per-user vs per-IP limits
- multi-instance support

Recommendation:

- move to Redis-backed limiter when scaling beyond one process

#### BL-10.2 Improve audit and observability

Refine:

- request tracing
- structured audit events
- privileged access visibility

#### BL-10.3 Add production hardening

Cover:

- secret management
- docs exposure rules
- HTTPS assumptions
- deployment checklist
- log retention policy

Dependencies:

- BL-04 through BL-09

## 14. Suggested Implementation Sequence

Follow this exact order:

1. BL-01
2. BL-02
3. BL-03
4. BL-04
5. BL-05
6. BL-06
7. BL-07
8. BL-08
9. BL-09
10. BL-10

Do not move BL-10 work ahead of BL-04 to BL-07 unless there is a production incident forcing it.

## 15. Suggested First Build Slice

If starting from scratch, the first implementation slice should be:

1. user model
2. chat model
3. OIDC/JWT config
4. JWT validation
5. current user resolution
6. `GET /me`

Why:

- it proves the identity model
- it proves the auth flow
- it proves the app can resolve real users before deeper route protection work

## 16. Definition Of Done

A backlog item is done only when:

- code is implemented
- dependencies are respected
- failure paths are handled
- access control behavior is explicit
- data ownership behavior is explicit
- acceptance criteria are verifiable

## 17. Immediate Next Task

The correct next task is:

- BL-01.1 through BL-01.3

That means:

- define OIDC trust assumptions
- define internal roles
- define the final `AuthContext` contract

Only after that should implementation continue.
