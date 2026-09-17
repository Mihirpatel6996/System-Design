# Task: Design a Notification System (LSP Focus)

---

## Problem Statement

Design a notification system with a base abstraction:

```python id="base_class"
class Notification:
    def send(self, message):
        pass
```

Create the following implementations:

* EmailNotification
* SMSNotification
* PushNotification
* SilentNotification (does nothing)

---

## Objective

1. First, design the system **incorrectly** (introduce an LSP violation)
2. Then fix it using proper abstraction

---

## Step 1 — Incorrect Design (LSP Violation)

### Implementation

```python id="bad_design"
class Notification:
    def send(self, message):
        raise NotImplementedError


class EmailNotification(Notification):
    def send(self, message):
        print(f"Email sent: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS sent: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"Push sent: {message}")


class SilentNotification(Notification):
    def send(self, message):
        raise Exception("Silent mode does not send messages")
```

---

## Why This is Wrong

The base contract says:

> `send(message)` should send a notification

But `SilentNotification`:

* Does not send
* Throws an exception
* Breaks expected behavior

---

## LSP Violation

> A subtype must be replaceable for its base type without breaking behavior

### Example Failure

```python id="failure_case"
def notify(notification: Notification):
    notification.send("Hello")

notify(SilentNotification())  # crashes
```

---

## Root Problem

`SilentNotification` is **not a true “is-a” Notification**

It violates the contract.

---

## Step 2 — Fix the Design

### Option 1 — Redefine Behavior (Best Practical Fix)

Allow "no-op" behavior as valid.

```python id="good_design"
class Notification:
    def send(self, message):
        pass


class EmailNotification(Notification):
    def send(self, message):
        print(f"Email sent: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS sent: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"Push sent: {message}")


class SilentNotification(Notification):
    def send(self, message):
        # intentionally does nothing
        pass
```

---

### Why This Works

* `send()` is still callable
* No exceptions
* Behavior is consistent with contract

System remains stable.

---

## Step 3 — Alternative Design (Stronger Abstraction)

Separate capability:

```python id="better_design"
from abc import ABC, abstractmethod

class Notification(ABC):

    @abstractmethod
    def send(self, message):
        pass


class RealNotification(Notification):
    pass


class EmailNotification(RealNotification):
    def send(self, message):
        print(f"Email sent: {message}")


class SMSNotification(RealNotification):
    def send(self, message):
        print(f"SMS sent: {message}")


class PushNotification(RealNotification):
    def send(self, message):
        print(f"Push sent: {message}")


class SilentNotification(Notification):
    def send(self, message):
        pass
```

---

## Step 4 — Think Before Coding

### Q1 — Is `SilentNotification` a valid subtype?

Yes, **only if**:

* It does not break expectations
* It behaves safely when substituted

If it throws or breaks flow → not valid

---

### Q2 — Should it inherit?

* If "doing nothing" is acceptable behavior → Yes
* If system requires actual delivery → No

Decision depends on:

> What the base contract guarantees

---

## Key Insight

LSP is not about inheritance.

It is about:

> Behavioral correctness under substitution

---

## Mental Model

Before inheriting, ask:

* Can this class fully replace the parent?
* Will any existing code break?

If yes → safe
If no → redesign

---

## Common Mistake

* Forcing inheritance for code reuse
* Ignoring behavioral expectations

---

## Final Takeaway

> Just because something *looks like a subtype* does not mean it *behaves like one*

That difference is exactly what LSP protects against.
