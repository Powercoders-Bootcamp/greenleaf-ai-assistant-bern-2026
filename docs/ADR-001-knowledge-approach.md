# ADR-001: How We Give the LLM Knowledge

## Status

Accepted

---

## Context

GreenLeaf Logistics requires an internal AI assistant ("Beat-Bot") to answer employee questions related to:

* HR policies (leave, working hours, expenses)
* Company handbook rules
* Basel-Stadt holidays and working days
* General operational procedures

The assistant must:

* Provide accurate, policy-compliant answers
* Avoid hallucinations
* Use official company data only
* Support natural language queries

The knowledge source is primarily:

* A company handbook (PDF → structured Markdown)
* A holiday-checking system for Basel-Stadt

The challenge is determining the most efficient and reliable way to provide this knowledge to the LLM.

---

## Options Considered

### 1. Keyword Search

**Description:**
Search the handbook using simple keyword matching and return matching text.

**Pros:**

* Easy to implement
* Fast and low cost
* Transparent and explainable
* No need for embeddings or vector databases

**Cons:**

* Cannot understand semantic meaning
* Fails if user wording differs from handbook wording
* Poor performance for complex or natural language queries
* Limited scalability for larger documents

**Fit for GreenLeaf:**
Not sufficient, as employees will ask questions in natural language, not exact keywords.

---

### 2. Long-Context Prompting (Context Stuffing)

**Description:**
Provide the entire handbook (or large parts of it) directly in the prompt.

**Pros:**

* Simple architecture (no retrieval system)
* No need for chunking or indexing
* Works for small datasets

**Cons:**

* Expensive (large token usage)
* Limited by model context window
* Reduced accuracy with too much information
* Difficult to maintain and scale
* Slower responses

**Fit for GreenLeaf:**
Not suitable, as the handbook is expected to grow. It would increase cost and reduce reliability.

---

### 3. Retrieval-Augmented Generation (RAG)

**Description:**
Store the handbook as structured chunks, embed them, and retrieve the most relevant sections at query time.

**Pros:**

* Semantic search (understands meaning, not just keywords)
* Scalable for large documents
* More accurate for natural language questions
* Reduces hallucination by grounding answers in retrieved content
* Efficient token usage (only relevant chunks are sent to the model)

**Cons:**

* More complex to implement (chunking, embeddings, vector store)
* Requires preprocessing and data cleaning
* Retrieval quality depends on chunking strategy

**Fit for GreenLeaf:**
Highly suitable. Employees ask varied natural language questions, and accurate retrieval of handbook content is critical.

---

## Final Decision

We chose a **hybrid architecture**:

### ✅ Retrieval-Augmented Generation (RAG) for handbook knowledge

### ✅ Tool-based approach for structured data (holiday checking)

---

## Architecture Overview

The system consists of:

1. **RAG Pipeline (Handbook)**

   * The PDF handbook is converted into structured Markdown
   * Text is split into chunks using headers and size-based splitting
   * Chunks are embedded using OpenAI embeddings
   * Stored in a FAISS vector database
   * Retrieved semantically based on user queries

2. **Tool: `search_handbook`**

   * Performs semantic retrieval from the vector store
   * Returns relevant handbook excerpts to the LLM

3. **Tool: `check_holiday`**

   * Deterministic Python function
   * Uses Basel-Stadt holiday API
   * Returns structured data:

     * holiday status
     * weekend status
     * non-working day status

4. **LLM with Tool Calling**

   * The model decides when to call:

     * `search_handbook` (for policies)
     * `check_holiday` (for date-related questions)
   * Can call multiple tools for combined questions

---

## Why This Decision

This hybrid approach provides:

### Accuracy

* Handbook answers are grounded in retrieved content
* Holiday answers are deterministic and API-based

### Reduced Hallucination

* The system prompt enforces tool usage
* The model is restricted from guessing

### Flexibility

* Supports natural language queries
* Handles combined questions (e.g., leave + date)

### Scalability

* Handbook can grow without increasing prompt size
* Retrieval remains efficient

### Separation of Concerns

* Unstructured knowledge → RAG
* Structured logic → tools

---

## Example Scenarios

### Example 1: Policy Question

**User:** Can I expense alcohol?

→ Tool used: `search_handbook`
→ Answer based on retrieved policy

---

### Example 2: Holiday Question

**User:** Is 2026-12-25 a holiday?

→ Tool used: `check_holiday`
→ Answer based on API result

---

### Example 3: Combined Question

**User:** Do I need to take leave on 2026-12-25?

→ Tools used:

1. `check_holiday`
2. `search_handbook`

→ Final answer combines:

* holiday status
* leave policy

---

## Consequences

### Positive

* High accuracy and reliability
* Strong control over hallucination
* Modular and extensible architecture
* Clear separation between data sources

### Negative

* Increased system complexity
* Requires preprocessing (Markdown conversion, chunking)
* Dependency on external API for holidays
* Need to maintain vector database

---

## Future Improvements

* Add multi language support
* Improve chunking strategy for better retrieval
* Add evaluation metrics (accuracy, tool usage success)
* Expand tools (e.g., expense calculator, internal systems)

---

## Conclusion

The hybrid approach using **RAG + tool calling** is the most efficient and scalable solution for GreenLeaf Logistics.

It ensures:

* accurate answers
* minimal hallucination
* efficient use of LLM capabilities

while maintaining flexibility for future system growth.
