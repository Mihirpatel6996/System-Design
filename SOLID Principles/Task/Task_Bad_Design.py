'''

Task: Fix a Broken Clinical RAG Pipeline (SRP Violation)
Problem Statement

You are given a single class that tries to do everything:

Reads patient notes
Generates embeddings
Stores them
Retrieves similar notes
Calls LLM
Logs everything

This is exactly how real systems start—and then collapse.

Your job:

Refactor this system using Single Responsibility Principle

'''

class ClinicalRAGSystem:

    def __init__(self):
        self.db = {}
        self.vector_store = {}

    def embed(self, text):
        # fake embedding
        return [len(text)]

    def store(self, patient_id, note):
        embedding = self.embed(note)
        self.vector_store[patient_id] = embedding
        self.db[patient_id] = note

    def retrieve(self, query):
        query_embedding = self.embed(query)

        # naive similarity
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



'''
What You Must Do
1. Identify Responsibilities

Write this down before coding:

What are the independent responsibilities?
What are the reasons each part will change?
2. Create Separate Classes

At minimum, think in terms of:

EmbeddingService
VectorStore
NoteRepository
Retriever
LLMService
Logger
Orchestrator (important)
3. Refactor run() into Orchestrator

The orchestration should:

data → embed → store → retrieve → generate → log

But it should NOT implement logic itself.

4. Keep It Runnable

No external libraries.

Simulate everything like the current code.

Step 4 — Validation (How I’ll Judge Your Solution)

Your solution is correct if:

1. You can answer this:
    “If I change embedding model → which class changes?”
    “If I switch to Redis → which class changes?”
    “If I change LLM provider → which class changes?”

If answer = only one class each → you did SRP correctly

2. No class should do more than one of:
    Data storage
    Business logic
    External communication
    Orchestration
3. Orchestrator should NOT contain logic

If you write:

if len(text) > 100:

inside orchestrator → you failed SRP

Step 5 — Think Like Production

After refactoring, answer:

Where would Kafka fit here?
Where would caching go?
What becomes a bottleneck first?
Deliverable

Send me:

Your refactored code
Your reasoning (which responsibility you split and why)
Hint (don’t skip thinking)

Most people make this mistake:

They split classes by “function name” instead of reason to change

Don’t do that.

'''