# L — Liskov Substitution Principle (LSP)

---

## Core Idea (Practical)

> If you replace a base class with its child,
> the system should **still behave correctly**

Not just compile. Not just run.

**Behavior must remain correct.**

---

## Mental Model

If this works:

```python id="base_usage"
def process(account):
    account.withdraw(100)
```

Then this must also work:

```python id="substitution"
process(SavingsAccount())
process(CurrentAccount())
process(FixedDepositAccount())  # potential failure point
```

If one subclass breaks expectations → **LSP is violated**

---

# 1. Naive Design (Looks Fine, Actually Broken)

## Base Class

```python id="base_account"
class Account:
    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass
```

---

## Child Implementations

```python id="savings"
class SavingsAccount(Account):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
```

```python id="fd"
class FixedDepositAccount(Account):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        raise Exception("Cannot withdraw before maturity")  # violation
```

---

# 2. Where It Breaks

System code:

```python id="system_code"
def process(account: Account):
    account.withdraw(100)
```

### Works

```python id="works"
process(SavingsAccount(1000))
```

### Fails

```python id="fails"
process(FixedDepositAccount(1000))  # runtime failure
```

---

# 3. Why This Violates LSP

Base class implies:

```text id="contract"
withdraw() is supported
```

But child changes behavior:

```text id="break_contract"
withdraw() → not always allowed
```

Result:

> Child is **not substitutable** for parent

---

# 4. Core Insight

LSP is about:

> Behavioral contracts, not method signatures

---

## Contract of Account (Implicit)

* deposit should work
* withdraw should work

`FixedDepositAccount` breaks this contract.

---

# 5. Fixing the Design (Correct LSP)

Do not patch the child.
Fix the abstraction.

---

## Step 1 — Separate Base Responsibility

```python id="fixed_base"
from abc import ABC, abstractmethod

class Account(ABC):

    @abstractmethod
    def deposit(self, amount):
        pass
```

---

## Step 2 — Introduce Capability-Based Abstraction

```python id="withdrawable"
class WithdrawableAccount(Account):

    @abstractmethod
    def withdraw(self, amount):
        pass
```

---

## Step 3 — Correct Implementations

```python id="fixed_savings"
class SavingsAccount(WithdrawableAccount):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
```

```python id="fixed_fd"
class FixedDepositAccount(Account):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    # no withdraw method
```

---

# 6. Safe System Design

```python id="safe_usage"
def process(account: WithdrawableAccount):
    account.withdraw(100)
```

Now:

```python id="safe_calls"
process(SavingsAccount(1000))  # valid
process(FixedDepositAccount(1000))  # prevented by design
```

---

# 7. Narrowing vs Expanding (Critical Concept)

## Narrowing (Violation)

Child reduces capability.

```python id="narrowing"
class Bird:
    def fly(self):
        pass

class Penguin(Bird):
    def fly(self):
        raise Exception("Cannot fly")  # violation
```

### Problem

* Parent guarantees ability
* Child removes it

→ LSP broken

---

## Expanding (Valid)

Child can add behavior without breaking contract.

```python id="expanding"
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def fly(self):
        pass
```

---

# 8. Design Rule

> Never force a child to implement behavior it cannot support

Instead:

* Split abstractions
* Model capabilities explicitly

---

# 9. Common Mistakes

* Designing base classes too broadly
* Forcing inheritance for code reuse
* Ignoring real-world constraints in models

---

# 10. System Design Insight

LSP ensures:

* Predictable behavior
* Safe polymorphism
* Reliable system evolution

Without LSP:

* Runtime failures
* Hidden bugs
* Fragile systems

---

# Final Takeaway

> If a subclass cannot fully honor the behavior of its parent,
> it should not inherit from it

---

## One-Line Summary

LSP = **Correct substitution without breaking behavior**
