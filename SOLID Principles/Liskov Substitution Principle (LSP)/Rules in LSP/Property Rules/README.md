# LSP — Property Rules

Liskov Substitution Principle is not only about method signatures.

It also governs **object properties and state behavior over time**.

Two critical rules:

1. **Class Invariant** → what must always remain true
2. **History Constraint** → how state is allowed to change

---

# 1. Class Invariant

## Definition

> A condition that must always hold true for an object
> before and after any method execution

---

## Example (Valid Invariant)

```python id="account_invariant"
class Account:
    def __init__(self, balance):
        self.balance = balance  # invariant: balance >= 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
```

### Implicit invariant

```
balance >= 0
```

---

## Violation in Child Class

```python id="invariant_violation"
class OverdraftAccount(Account):

    def withdraw(self, amount):
        self.balance -= amount  # allows negative balance
```

---

## Why This Breaks LSP

* Parent guarantees: balance never goes negative
* Child breaks that guarantee

System relying on parent behavior may fail.

---

## Correct Design

Either:

### Option 1 — Relax invariant in parent

```python id="relaxed_parent"
class Account:
    def __init__(self, balance):
        self.balance = balance  # can be negative
```

### Option 2 — Separate abstraction

```python id="split_design"
class StrictAccount(Account):
    pass

class OverdraftAccount(Account):
    pass
```

---

## Key Rule

> Child must **preserve or strengthen invariants**, never weaken them

---

# 2. History Constraint

## Definition

> A subclass must not allow state transitions
> that are **not possible in the base class**

---

## Example (Violation)

```python id="history_violation"
class ReadOnlyDocument:

    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content
```

Child class:

```python id="bad_child"
class EditableDocument(ReadOnlyDocument):

    def write(self, new_content):
        self.content = new_content  # state mutation allowed
```

---

## Why This Breaks LSP

Parent behavior:

```
content never changes after creation
```

Child behavior:

```
content can change
```

This introduces a **new state transition** not allowed by parent.

---

## Real Failure Scenario

```python id="history_break"
def process(doc: ReadOnlyDocument):
    original = doc.read()
    # assume content won't change
    later = doc.read()
    assert original == later  # breaks for EditableDocument
```

---

## Correct Design

### Option 1 — Separate abstractions

```python id="history_fix"
class Document:
    def read(self):
        pass


class ReadOnlyDocument(Document):
    pass


class EditableDocument(Document):
    def write(self, content):
        pass
```

---

## Key Rule

> Subclass must not introduce **unexpected state changes**

---

# 3. Combined View

| Rule               | What it Controls  | Violation Example        |
| ------------------ | ----------------- | ------------------------ |
| Class Invariant    | Valid state       | balance becomes negative |
| History Constraint | State transitions | read-only → mutable      |

---

# 4. Mental Model

Think in terms of **guarantees over time**:

* Invariant → “This is always true”
* History → “This will never happen”

If a subclass breaks either → LSP violation

---

# 5. System Design Insight

These rules are critical in:

* Financial systems (balance constraints)
* Medical systems (patient state validity)
* Distributed systems (state consistency)
* APIs (response guarantees over time)

---

# 6. Common Mistakes

* Ignoring implicit invariants
* Adding mutation to immutable objects
* Allowing invalid states in child classes
* Mixing read-only and editable behavior

---

# 7. Final Takeaway

> LSP is not just about methods
> It is about **state correctness over time**

---

## One-Line Summary

* Invariant → always true
* History → always consistent

Break either → break substitution
