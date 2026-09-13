# Step 4: Polymorphism — What It Actually Means

Polymorphism is about:

> Writing code that works with **multiple types through a common interface**

It is not:

* Theory-heavy abstraction
* Just “same method name”

---

## Core Idea

> One piece of code → works with many implementations

---

## Real System Mapping

Consider an LLM system.

### Without Polymorphism (Bad Design)

```python
if provider == "gemini":
    call_gemini()
elif provider == "groq":
    call_groq()
```

Problems:

* Tight coupling
* Hard to extend
* Violates open/closed principle

---

### With Polymorphism (Correct Design)

```python
def generate(llm, prompt):
    return llm.generate(prompt)
```

Where:

```python
class GeminiLLM:
    def generate(self, prompt):
        pass

class GroqLLM:
    def generate(self, prompt):
        pass
```

Meaning:

* Same interface (`generate`)
* Different implementations
* Caller doesn’t care which one is used

---

## Types of Polymorphism (Conceptual)

### 1. Compile-Time Polymorphism

* Decision made before execution
* Typically achieved via **method overloading**

---

### 2. Runtime Polymorphism

* Decision made during execution
* Achieved via **method overriding**

---

## Important Reality (Python vs Java/C++)

| Concept                   | Java/C++  | Python              |
| ------------------------- | --------- | ------------------- |
| Method Overloading        | Supported | Not truly supported |
| Method Overriding         | Supported | Supported           |
| Compile-time Polymorphism | Yes       | Not really          |
| Runtime Polymorphism      | Yes       | Yes (core concept)  |

---

## Method Overriding (Actual Polymorphism in Python)

Child class changes behavior of parent.

```python
class LLM:
    def generate(self, prompt):
        raise NotImplementedError

class GeminiLLM(LLM):
    def generate(self, prompt):
        return "Gemini response"

class GroqLLM(LLM):
    def generate(self, prompt):
        return "Groq response"
```

Usage:

```python
def run(llm):
    print(llm.generate("Hello"))

run(GeminiLLM())
run(GroqLLM())
```

👉 Same function, different behavior at runtime.

---

## Method Overloading (Python Reality)

Python does not support true method overloading like Java.

This will NOT work:

```python
class Example:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):   # overrides previous
        return a + b + c
```

---

### How Python Handles It (Workarounds)

#### Default Arguments

```python
class Example:
    def add(self, a, b, c=None):
        if c is None:
            return a + b
        return a + b + c
```

---

#### Variable Arguments

```python
class Example:
    def add(self, *args):
        return sum(args)
```

---

👉 This is not true overloading — just flexible function design.

---

## Key Design Insight

Polymorphism removes:

* Condition-based logic (`if/else`)
* Tight coupling
* Repetitive code

And replaces it with:

* Interface-based design
* Extensibility
* Cleaner architecture

---

## Where You Already Use It

* LLM providers (Gemini, Groq, OpenAI)
* Payment gateways
* Notification systems (Email, SMS, Push)
* Logging systems

---

## Common Mistakes

* Thinking same method name = polymorphism
* Writing condition-heavy code instead of interfaces
* Not designing a proper base interface
* Mixing responsibilities

---

## One-Line Takeaway

Polymorphism = write code once, support multiple behaviors

---

## Final Insight

Encapsulation → controls data
Abstraction → hides complexity
Inheritance → defines relationships
Polymorphism → enables flexible behavior

---

Next step: combining all four principles into a real system design (end-to-end example)
