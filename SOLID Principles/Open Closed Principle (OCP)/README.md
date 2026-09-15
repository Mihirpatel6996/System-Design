# Open/Closed Principle (OCP)

---

## Core Idea

> Software entities should be **open for extension, closed for modification**

Meaning:

* You should be able to **add new behavior**
* Without **changing existing code**

---

## Why This Matters in Systems

Without OCP:

* Every new feature → modify existing logic
* High risk of breaking working code
* Increasing `if/else` complexity

With OCP:

* Add new functionality safely
* Existing system remains stable
* Scales cleanly with new requirements

---

## Classic Violation

```python
def generate(provider, prompt):
    if provider == "gemini":
        return f"Gemini: {prompt}"
    elif provider == "groq":
        return f"Groq: {prompt}"
```

### Problem

* Adding a new provider requires modifying this function
* Violates OCP
* Becomes unmaintainable as cases grow

---

## OCP-Compliant Design

### Step 1 — Define Abstraction

```python
class LLM:
    def generate(self, prompt):
        pass
```

---

### Step 2 — Extend via New Classes

```python
class GeminiLLM(LLM):
    def generate(self, prompt):
        return f"Gemini: {prompt}"


class GroqLLM(LLM):
    def generate(self, prompt):
        return f"Groq: {prompt}"
```

---

### Step 3 — Use Polymorphism

```python
def generate(llm: LLM, prompt):
    return llm.generate(prompt)
```

---

### Result

* Add new provider → create new class
* No change to existing code
* Fully OCP compliant

---

## Real System Mapping

### In your LLM + RAG system

Instead of:

```python
if model == "gemini":
    ...
elif model == "groq":
    ...
```

You do:

```python
pipeline = Pipeline(llm=GeminiLLM())
pipeline = Pipeline(llm=GroqLLM())
```

---

### Other Examples

| Component     | OCP Application               |
| ------------- | ----------------------------- |
| LLM Providers | Add new model via new class   |
| Retrievers    | Swap DB (vector, SQL, hybrid) |
| Tools         | Add new tool without changes  |
| Notification  | Email, SMS, PagerDuty         |

---

## Design Pattern Behind OCP

OCP is usually implemented using:

* **Interfaces / Abstract Base Classes**
* **Polymorphism**
* **Strategy Pattern**

---

## Mental Model

Bad approach:

> “Modify existing code to support new case”

Good approach:

> “Extend system by adding new module”

---

## Trade-offs

### Pros

* Safe extensibility
* Reduced regression risk
* Cleaner architecture

### Cons

* More classes
* Requires upfront abstraction
* Can feel heavy for small systems

---

## When NOT to Apply Strictly

Avoid over-engineering when:

* Only 1–2 variations exist
* No expected future extension
* Prototype stage

---

## Common Mistakes

* Using inheritance without abstraction
* Creating deep class hierarchies unnecessarily
* Adding abstraction without real extension need

---

## Quick Checklist

Before writing code, ask:

* Will this logic grow with new cases?
* Am I modifying existing code for every new feature?
* Can I add behavior without touching current code?

If not → apply OCP

---

## One-Line Takeaway

> Don’t modify working code to add features — **extend it**

---

## Final Insight

OCP is what separates:

* Small scripts → scalable systems

Without OCP:

* Systems become rigid

With OCP:

* Systems evolve safely over time
