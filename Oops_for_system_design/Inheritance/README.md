# Step 3: Inheritance — What It Actually Means

Inheritance is about:

> Reusing behavior **only when there is a true “is-a” relationship**

It is **not** for:

* Reducing typing
* Sharing code arbitrarily

---

## Core Example

```
LoadRunnerTest is a PerformanceTest
```

This means:

* LoadRunnerTest should behave like a PerformanceTest
* It can extend or refine behavior, not violate it

---

## super() — Reusing Parent Logic

When the parent class has useful logic, the child should reuse it.

### Parent

```python
class PerformanceTest:

    def start(self):
        print("Common setup")
```

### Child

```python
class LoadRunnerTest(PerformanceTest):

    def start(self):
        super().start()
        print("LoadRunner specific setup")
```

### Meaning

* Parent logic is reused
* Child adds additional behavior
* Execution order is controlled

---

## Method Overriding

A child class can completely change parent behavior.

```python
class JMeterTest(PerformanceTest):

    def start(self):
        print("Custom JMeter start logic")
```

This is called:

> Method overriding — child replaces parent implementation

---

## Critical Rule (Liskov Substitution Principle)

Use inheritance only if:

> A child object can replace a parent object without breaking the system

This ensures:

* Consistency
* Reliability
* Predictable behavior

---

## Inheritance vs Composition

This is a key system design decision.

### Bad Inheritance

```python
class Engine:
    pass

class Car(Engine):   # Incorrect relationship
    pass
```

Reason:

* A car is not an engine
* Relationship is incorrectly modeled

---

### Correct Design (Composition)

```python
class Engine:
    pass

class Car:
    def __init__(self):
        self.engine = Engine()
```

This is:

> Composition — “has-a” relationship

---

## When to Use Inheritance

Use inheritance only when:

* A clear hierarchy exists
* Behavior is naturally shared
* Substitution is valid (LSP holds)

---

## When to Avoid Inheritance

Avoid inheritance when:

* Relationship is “has-a”
* You only want code reuse
* Behavior differs significantly
* Future changes may break hierarchy

---

## Real System Mapping

### Good Inheritance

* Base: `LLM`
* Children: `GeminiLLM`, `GroqLLM`

Reason:

* All represent the same concept
* Share core behavior
* Can be used interchangeably

---

### Bad Inheritance

* `User` inheriting from `Database`
* `TestRun` inheriting from `Logger`

Reason:

* No “is-a” relationship
* Violates system design principles

---

## Common Mistakes

* Using inheritance for convenience
* Deep inheritance chains
* Overriding without understanding parent behavior
* Breaking LSP unintentionally

---

## Practical Insight

Inheritance tightly couples classes.

This means:

* Changes in parent affect children
* Poor design propagates quickly

👉 Prefer composition unless inheritance is clearly justified

---

## One-Line Takeaway

Inheritance = reuse behavior **only when the relationship is fundamentally correct**

---

## Final Insight

Encapsulation protects data
Abstraction hides complexity
Inheritance structures relationships

Misuse of inheritance leads to rigid, fragile systems

---

Next step: Polymorphism — how systems handle multiple behaviors through a single interface
