# Open/Closed Principle (OCP)

---

## Context

Single Responsibility Principle (SRP) gave you **clean boundaries**.

Now OCP tells you:

> How to **extend those boundaries without breaking them**

---

## Core Idea

> Open for extension, closed for modification

Ignore the textbook phrasing. The real meaning:

* You should be able to **add new behavior**
* Without **changing existing code**

---

## 1. Problem (Real System Context)

In your RAG pipeline:

```text id="rag_problem"
Retriever → returns best_match_id
```

Now product asks:

* Add keyword-based retrieval
* Add cosine similarity
* Add hybrid retrieval

Naive approach:

```python id="rag_bad"
if strategy == "length":
    ...
elif strategy == "keyword":
    ...
elif strategy == "cosine":
    ...
```

This is where systems start breaking.

---

## 2. Simple Example — Payment Processing

### Initial Requirement

* Only Credit Card payments

---

## Naive Implementation (OCP Violation)

```python id="bad_payment"
class PaymentProcessor:

    def process(self, payment_type, amount):

        if payment_type == "credit_card":
            return f"Processing credit card payment of {amount}"

        elif payment_type == "upi":
            return f"Processing UPI payment of {amount}"

        elif payment_type == "paypal":
            return f"Processing PayPal payment of {amount}"

        else:
            raise ValueError("Unsupported payment type")
```

---

## 3. What Breaks at Scale

At small scale:

* Works fine

At real scale:

* 15+ payment methods
* Country-specific logic
* Retry rules per type

Result:

```text id="scale_problem"
PaymentProcessor → 500+ lines
```

Risk:

> One change can break all payment flows

---

## 4. Apply OCP (Step-by-Step)

### Step 1 — Abstraction

```python id="payment_interface"
from abc import ABC, abstractmethod

class PaymentMethod(ABC):

    @abstractmethod
    def process(self, amount):
        pass
```

---

### Step 2 — Concrete Implementations

```python id="credit"
class CreditCardPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing credit card payment of {amount}"
```

```python id="upi"
class UPIPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing UPI payment of {amount}"
```

```python id="paypal"
class PayPalPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing PayPal payment of {amount}"
```

---

### Step 3 — Processor (Closed for Modification)

```python id="processor"
class PaymentProcessor:

    def process(self, payment_method: PaymentMethod, amount):
        return payment_method.process(amount)
```

---

## 5. Extending the System

New requirement:

> Add Crypto payments

```python id="crypto"
class CryptoPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing crypto payment of {amount}"
```

No existing code is modified.

---

## 6. Key Shift

Before:

```text id="before"
Behavior controlled by IF/ELSE
```

After:

```text id="after"
Behavior controlled by POLYMORPHISM
```

This is the core of OCP.

---

## 7. Why This Matters in Real Systems

In production:

* Payment team adds new method → no core changes
* Risk logic evolves → isolated changes
* New regions → new classes, not rewrites

---

## 8. Trade-offs

### Pros

* Safe extensibility
* Isolation of logic
* Enables parallel development

---

### Cons

* More classes
* Indirection increases
* Slightly harder to trace initially

---

## 9. Mental Trigger for OCP

Whenever you see:

```python id="trigger"
if type == "X":
elif type == "Y":
elif type == "Z":
```

That is your signal:

> This logic will grow → apply OCP

---

## 10. Mapping to Your RAG System

These are OCP violations:

```python id="rag_violation"
if model == "gemini":
if retriever == "cosine":
if alert_type == "email":
```

Correct approach:

* Create interfaces
* Add implementations
* Use polymorphism

---

## Final Insight

OCP is not about abstraction for the sake of it.

It is about:

> Preventing system breakage when requirements grow

---

## One-Line Takeaway

> Stop modifying existing code for new behavior — start extending it
