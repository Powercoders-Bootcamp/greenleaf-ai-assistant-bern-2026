# ADR-001: Frontend Build Tool Selection (Vite)

## Status
**Accepted**

---

## Context

Our team is building a frontend chat interface for the **GreenLeaf AI Assistant**.

The system must:
- Respond quickly (chat UX)
- Be simple to develop and maintain (bootcamp constraints)
- Allow fast iteration (Agile environment)
- Integrate easily with backend API (`/chat`)

The bootcamp is project-based and Agile, so **speed and simplicity** are more important than complex enterprise setups.

---

## Decision

We chose **Vite** as the frontend build tool.

---

## Rationale

### 1. Fast Development Server
- Instant startup  
- Hot Module Replacement (HMR)  

➡️ Ideal for rapid UI iteration

---

### 2. Lightweight Setup
- Minimal configuration  
- No complex bundler setup (like Webpack)

➡️ Saves development time

---

### 3. Modern Stack Support
- React  
- TypeScript  
- ES Modules  

➡️ Works out of the box

---

### 4. Better Developer Experience
- Clean project structure  
- Faster debugging  
- Immediate feedback loop  

➡️ Improves productivity

---

## Alternatives Considered

### Next.js

**Pros**
- Server-side rendering (SSR)
- Built-in routing
- Production-ready features

**Cons**
- Overkill for a simple chat UI
- More complex setup
- Slower onboarding for the team

➡️ Not suitable for MVP

---

### Create React App (CRA)

**Pros**
- Familiar setup

**Cons**
- Slow build times
- Outdated ecosystem
- Poor developer experience

➡️ Not suitable for modern development

---

## Consequences

### ✅ Pros
- Fast development cycle  
- Simple architecture  
- Quick iteration and testing  

### ❌ Cons
- No server-side rendering (SSR)  
- Less scalable for large enterprise apps  

---

## Final Justification

Vite best fits our needs for:
- Rapid prototyping  
- Simple architecture  
- Fast UI iteration  

This aligns with:
- Agile workflow  
- Bootcamp constraints  
- MVP-focused development
