# Putting All 4 OOP Principles Together — LLM + RAG + Tools System

This document builds a system similar to a real-world AI pipeline:

* User provides a query
* System:

  1. Retrieves context (RAG)
  2. Calls an LLM
  3. Optionally uses tools

The goal is to show **exactly where each OOP principle applies**.

---

# 1. Abstraction — Define Contracts

We start by defining interfaces (what the system can do, not how).

## LLM Interface

```python
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
```

## Retriever Interface

```python
class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass
```

## Tool Interface

```python
class Tool(ABC):
    @abstractmethod
    def execute(self, input_data: str) -> str:
        pass
```

### Meaning

* Defines capabilities
* No implementation details
* Forces consistency

This is **abstraction**.

---

# 2. Inheritance — Concrete Implementations

## LLM Implementations

```python
class GeminiLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Gemini]: {prompt}"


class GroqLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Groq]: {prompt}"
```

## Retriever Implementation

```python
class SimpleRetriever(Retriever):
    def retrieve(self, query: str) -> str:
        return f"Context for: {query}"
```

## Tool Implementation

```python
class CalculatorTool(Tool):
    def execute(self, input_data: str) -> str:
        return f"Calculated result for {input_data}"
```

### Meaning

* Each class **is-a** specific type
* Reuses structure from base classes

This is **inheritance**.

---

# 3. Encapsulation — Control Internal Workflow

Now we build the orchestrator.

```python
class RAGPipeline:
    def __init__(self, llm: LLM, retriever: Retriever, tools: list[Tool]):
        self._llm = llm
        self._retriever = retriever
        self._tools = tools

    def query(self, user_query: str) -> str:
        context = self._retrieve_context(user_query)
        enriched_prompt = self._build_prompt(user_query, context)
        return self._generate_response(enriched_prompt)

    def _retrieve_context(self, query):
        return self._retriever.retrieve(query)

    def _build_prompt(self, query, context):
        return f"Context: {context}\nQuery: {query}"

    def _generate_response(self, prompt):
        return self._llm.generate(prompt)
```

### What is Encapsulated

* Retrieval logic
* Prompt construction
* LLM interaction

External usage:

```python
pipeline.query("your question")
```

This is **encapsulation** — internal complexity is hidden.

---

# 4. Polymorphism — Plug-and-Play Behavior

```python
pipeline1 = RAGPipeline(GeminiLLM(), SimpleRetriever(), [])
pipeline2 = RAGPipeline(GroqLLM(), SimpleRetriever(), [])
```

Same call:

```python
pipeline1.query("What is AI?")
pipeline2.query("What is AI?")
```

Different behavior:

* Gemini response
* Groq response

No conditional logic required.

This is **polymorphism**.

---

# 5. Extending with Tools

```python
class RAGPipeline:
    def __init__(self, llm: LLM, retriever: Retriever, tools: list[Tool]):
        self._llm = llm
        self._retriever = retriever
        self._tools = tools

    def query(self, user_query: str) -> str:
        context = self._retriever.retrieve(user_query)

        if "calculate" in user_query:
            return self._use_tool(user_query)

        prompt = f"Context: {context}\nQuery: {user_query}"
        return self._llm.generate(prompt)

    def _use_tool(self, query):
        for tool in self._tools:
            return tool.execute(query)
```

### Where Polymorphism Happens

```python
tool.execute()
```

You can pass:

* CalculatorTool
* DBTool
* SearchTool

Same method → different behavior.

---

# 6. Clean Mapping of OOP Principles

| Principle     | Role in System                    |
| ------------- | --------------------------------- |
| Encapsulation | Pipeline hides internal logic     |
| Abstraction   | Interfaces (LLM, Tool, Retriever) |
| Inheritance   | Gemini, Groq, Calculator classes  |
| Polymorphism  | Same call, different behavior     |

---

# 7. System Benefits

## Swap LLM Easily

```python
RAGPipeline(GeminiLLM(), ...)
RAGPipeline(GroqLLM(), ...)
```

---

## Add New Tool Without Breaking System

```python
class DBTool(Tool):
    def execute(self, input_data):
        return "DB result"
```

No pipeline changes required.

---

## Extend Retriever

```python
class VectorDBRetriever(Retriever):
    def retrieve(self, query):
        return "Vector DB context"
```

---

# 8. What This Design Avoids

* Large if/else blocks
* Tight coupling
* Code duplication
* Breaking existing logic when extending

---

# 9. Real-World Equivalent

This structure directly maps to:

* LangChain abstractions
* LangGraph workflows
* MCP tool systems
* Multi-LLM orchestration

This is essentially a **basic agent framework**.

---

# 10. Design Observations (Critical)

* Pipeline hides complexity → encapsulation
* Interfaces prevent chaos → abstraction
* Implementations extend behavior → inheritance
* Runtime flexibility → polymorphism

---

# 11. Self-Check Questions

You should be able to answer:

1. Why does the pipeline hide internal methods?
2. Why is there no `if llm == "gemini"`?
3. Why does adding a new tool not break existing code?
4. Where exactly is polymorphism happening?

---

# Final Insight

Encapsulation protects the system
Abstraction defines structure
Inheritance organizes relationships
Polymorphism enables flexibility

Together, they form the foundation of scalable system design.
