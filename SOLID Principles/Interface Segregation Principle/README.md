# Interface Segregation Principle (ISP)

> **“Clients should not be forced to depend on interfaces they do not use.”**

---

## 1. Core Idea (Intuition)

Instead of creating **one large, general-purpose interface**, break it into **smaller, specific interfaces**.

Each class should only implement what it actually needs.

---

## 2. The Problem (Violation of ISP)

### Bad Design — Fat Interface

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def eat(self):
        pass
```

Now imagine:

```python
class Human(Worker):
    def work(self):
        print("Working")

    def eat(self):
        print("Eating")
```

Looks fine.

But:

```python
class Robot(Worker):
    def work(self):
        print("Working")

    def eat(self):
        raise NotImplementedError("Robots don't eat")
```

### Problem:

* Robot is **forced to implement `eat()`**
* This violates ISP
* Leads to:

  * Dummy implementations
  * Exceptions
  * Confusing design

---

## 3. The Fix (Apply ISP)

### Split the Interface

```python
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass
```

Now:

```python
class Human(Workable, Eatable):
    def work(self):
        print("Working")

    def eat(self):
        print("Eating")

class Robot(Workable):
    def work(self):
        print("Working")
```

### Result:

* No unnecessary methods
* Clean separation of responsibilities
* Flexible design

---

## 4. Real-World Analogy

Think of a **remote control**:

* Bad design → One remote with 50 buttons (most unused)
* Good design → Separate remotes:

  * TV remote
  * AC remote
  * Sound system remote

Each device uses only what it needs.

---

## 5. When ISP is Violated

Watch for these signals:

* Classes implementing methods they don’t use
* `pass` or `NotImplementedError` inside methods
* Large interfaces with unrelated responsibilities
* Conditional logic based on type (if robot → skip eat)

---

## 6. Benefits of ISP

* Improves **code readability**
* Reduces **coupling**
* Makes code easier to **maintain and extend**
* Prevents **accidental breaking changes**
* Works well with **Dependency Injection**

---

## 7. ISP + Other SOLID Principles

* **SRP** → Keeps responsibilities small
* **LSP** → No fake/unsupported behavior (like Robot eating)
* **DIP** → Depends on small, focused abstractions

---

## 8. Practical Use in Your Projects (Important for You)

### In AI / RAG Systems

Instead of:

```python
class AIService:
    def embed(self): pass
    def generate(self): pass
    def retrieve(self): pass
```

Do:

```python
class Embedder:
    def embed(self): pass

class Generator:
    def generate(self): pass

class Retriever:
    def retrieve(self): pass
```

Now:

* Swap embedding model independently
* Change LLM without affecting retrieval
* Better for microservices / modular design

---

## 9. Interview / Quick Definition

> ISP means **breaking large interfaces into smaller ones so that clients only depend on what they actually use.**

---

## 10. One-Line Summary

> “Don’t force a class to implement methods it doesn’t need.”

---

## 11. Quick Self-Test

* Does my class implement unused methods? → ❌
* Do I see `NotImplementedError`? → ❌
* Can I split this interface logically? → ✅

---

## Final Thought

ISP is about **respecting boundaries**.

When you design interfaces properly:

* Your system becomes **plug-and-play**
* Your components become **independent**
* Your architecture becomes **clean and scalable**
