# LSP — Method Rules

Liskov Substitution Principle is not just about class structure.

It also defines **how method behavior must be preserved** when overridden.

Two critical rules:

1. **Precondition Rule** → what must be true *before* a method runs
2. **Postcondition Rule** → what must be true *after* a method runs

---

# 1. Precondition Rule

## Definition

> A subclass must **not strengthen (tighten)** preconditions

Meaning:

* It should **not require more strict input conditions** than the parent
* It can accept the same or more relaxed inputs

---

## Example (Base Class)

```python id="pre_base"
class PaymentProcessor:
    def process(self, amount):
        # accepts any positive amount
        if amount <= 0:
            raise ValueError("Invalid amount")
        print(f"Processing payment: {amount}")
```

---

## Violation (Strengthening Precondition)

```python id="pre_bad"
class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        # now requires minimum 100
        if amount < 100:
            raise ValueError("Minimum amount is 100")
        print(f"Processing credit card payment: {amount}")
```

---

## Why This Breaks LSP

Caller expects:

```id="pre_expect"
any positive amount should work
```

But child says:

```id="pre_break"
only amount >= 100 works
```

This makes the subclass **less usable than the parent**.

---

## Correct Approach

```python id="pre_good"
class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        # same or weaker condition
        if amount <= 0:
            raise ValueError("Invalid amount")
        print(f"Processing credit card payment: {amount}")
```

---

## Key Rule

> Precondition can be **weaker or equal**, never stronger

---

# 2. Postcondition Rule

## Definition

> A subclass must **not weaken postconditions**

Meaning:

* It must fulfill at least what the parent guarantees
* It can provide stronger guarantees, but not fewer

---

## Example (Base Class)

```python id="post_base"
class FileWriter:
    def write(self, data):
        # guarantees data is written
        print("Data written successfully")
        return True
```

---

## Violation (Weakening Postcondition)

```python id="post_bad"
class UnreliableFileWriter(FileWriter):
    def write(self, data):
        print("Trying to write...")
        return False  # does not guarantee success
```

---

## Why This Breaks LSP

Caller expects:

```id="post_expect"
write() returns True if successful
```

But child:

```id="post_break"
returns False unpredictably
```

Now system logic depending on success breaks.

---

## Correct Approach (Strengthening Allowed)

```python id="post_good"
class SafeFileWriter(FileWriter):
    def write(self, data):
        print("Data written with backup")
        return True  # same or stronger guarantee
```

---

## Key Rule

> Postcondition can be **stronger or equal**, never weaker

---

# 3. Combined View

| Rule          | What it Controls   | Not Allowed             |
| ------------- | ------------------ | ----------------------- |
| Precondition  | Input requirements | More restrictive inputs |
| Postcondition | Output guarantees  | Weaker guarantees       |

---

# 4. Mental Model

Think in terms of **promises**:

* Precondition → “What you must give me”
* Postcondition → “What I guarantee you”

LSP ensures:

* Subclass asks for **less or equal**
* Subclass gives **more or equal**

---

# 5. Practical System Insight

These rules appear everywhere:

### APIs

* Precondition → request validation
* Postcondition → response guarantees

### Databases

* Precondition → query constraints
* Postcondition → data consistency

### LLM Systems

* Precondition → prompt format
* Postcondition → structured output

Breaking these leads to:

* runtime errors
* unreliable systems
* integration failures

---

# 6. Common Mistakes

* Adding stricter validation in subclasses
* Returning incomplete or inconsistent results
* Ignoring parent guarantees
* Changing method semantics silently

---

# 7. Final Takeaway

> Subclasses must not demand more and must not deliver less

---

## One-Line Summary

* Precondition → don’t ask for more
* Postcondition → don’t give less

Break either → LSP violation
