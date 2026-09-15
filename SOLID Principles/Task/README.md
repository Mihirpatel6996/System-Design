# Task: Fix a Broken Clinical RAG Pipeline (SRP Violation)

---

## Problem Statement

You are given a **single class** that tries to do everything:

* Reads patient notes
* Generates embeddings
* Stores them
* Retrieves similar notes
* Calls LLM
* Logs everything

This is how many real systems begin — and eventually become unmaintainable.

Your objective:

> Refactor this system using the **Single Responsibility Principle (SRP)**

---

## Step 1 — Understand the Bad Design

Run and analyze the following implementation:

```python id="bad_design"
class ClinicalRAGSystem:

    def __init__(self):
        self.db = {}
        self.vector_store = {}

    def embed(self, text):
        return [len(text)]

    def store(self, patient_id, note):
        embedding = self.embed(note)
        self.vector_store[patient_id] = embedding
        self.db[patient_id] = note

    def retrieve(self, query):
        query_embedding = self.embed(query)

        best_match = None
        best_score = float("inf")

        for pid, emb in self.vector_store.items():
            score = abs(emb[0] - query_embedding[0])
            if score < best_score:
                best_score = score
                best_match = pid

        return self.db.get(best_match, "")

    def call_llm(self, context, query):
        return f"LLM Response based on [{context}] for query [{query}]"

    def log(self, msg):
        print(f"LOG: {msg}")

    def run(self, patient_id, note, query):
        self.log("Storing note")
        self.store(patient_id, note)

        self.log("Retrieving context")
        context = self.retrieve(query)

        self.log("Calling LLM")
        response = self.call_llm(context, query)

        self.log("Done")
        return response
```

---

## Step 2 — Objective

Refactor this into a **SRP-compliant design**.

---

## Constraints

* Do not over-engineer
* Target **4–6 components maximum**
* Keep the system simple and runnable
* No external libraries

---

## Target Architecture

Aim for a structure like:

```text id="target_arch"
Ingestion → Embedding → Storage → Retrieval → LLM → Orchestrator
                         ↑
                       Logger
```

---

## Step 3 — Implementation Guidelines

### 1. Identify Responsibilities

Before coding, define:

* What are the independent responsibilities?
* What are the reasons each part will change?

---

### 2. Create Separate Components

At minimum, consider:

* EmbeddingService
* VectorStore
* NoteRepository
* Retriever
* LLMService
* Logger
* Orchestrator

---

### 3. Refactor Orchestration

The flow should be:

```text id="flow_logic"
data → embed → store → retrieve → generate → log
```

The orchestrator should:

* Coordinate flow only
* Not implement business logic

---

### 4. Keep It Runnable

* No frameworks
* No external dependencies
* Simulate behavior like the original code

---

## Step 4 — Validation Criteria

### 1. Change Isolation

You should be able to answer:

* If embedding model changes → which class changes?
* If storage moves to Redis → which class changes?
* If LLM provider changes → which class changes?

Correct answer:

> Only one class per change

---

### 2. Responsibility Boundaries

No class should handle more than one of:

* Data storage
* Business logic
* External communication
* Orchestration

---

### 3. Orchestrator Discipline

The orchestrator must not contain logic like:

```python id="invalid_logic"
if len(text) > 100:
```

If it does, SRP is violated.

---

## Step 5 — Think Like Production

After refactoring, consider:

1. Where would Kafka fit in this architecture?
2. Where would caching be introduced?
3. What component becomes the first bottleneck?

---

## Deliverable

Submit:

1. Refactored code
2. Explanation of how responsibilities were split
3. Justification based on “reason to change”

---

## Hint

Avoid this mistake:

> Splitting classes by function names instead of **reasons to change**

Focus on:

* Change isolation
* Responsibility boundaries
* System evolution

---

## Final Insight

This exercise is not about code organization.

It is about:

> Designing systems that can evolve without breaking under change
