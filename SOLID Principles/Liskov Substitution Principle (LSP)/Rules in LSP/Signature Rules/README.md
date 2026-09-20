# LSP Signature Rules

These rules ensure that **subclasses remain safely substitutable** for their base classes.

They define how method signatures can (and cannot) change in child classes.

---

## Core Idea

When overriding a method, the child must **not break the expectations** set by the parent.

This applies to:

* Method arguments
* Return types
* Exceptions

---

# 1. Method Argument Rule (Input)

## Rule

> Child class should **not narrow the input requirements**

---

## Violation (Narrowing Input)

```python id="arg_bad"
class PaymentProcessor:
    def process(self, amount: float):
        print("Processing payment")


class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: int):  # narrower type
        print("Processing credit card payment")
```

### Problem

* Parent accepts `float`
* Child accepts only `int`

Code using parent:

```python id="arg_fail"
def execute(processor: PaymentProcessor):
    processor.process(10.5)

execute(CreditCardProcessor())  # breaks expectation
```

---

## Correct Approach

```python id="arg_good"
class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: float):
        print("Processing credit card payment")
```

---

## Insight

> Inputs can be the **same or more general**, but never more restrictive

---

# 2. Return Type Rule (Output)

## Rule

> Child class can return a **more specific type** (covariance)

---

## Covariance Explained

* Parent returns general type
* Child returns a more specific subtype

---

## Example

```python id="return_good"
class Animal:
    pass


class Dog(Animal):
    pass


class AnimalFactory:
    def create(self) -> Animal:
        return Animal()


class DogFactory(AnimalFactory):
    def create(self) -> Dog:  # more specific
        return Dog()
```

### Why This Works

* System expects `Animal`
* Child gives `Dog` (which is an `Animal`)

No break in behavior.

---

## Violation (Returning More Generic)

```python id="return_bad"
class DogFactory(AnimalFactory):
    def create(self) -> object:  # too generic
        return "not even an Animal"
```

### Problem

* Parent guarantees `Animal`
* Child weakens that guarantee

---

## Insight

> Output can be **more specific**, not more general

---

# 3. Exception Rule

## Rule

> Child class should **not throw broader or unexpected exceptions**

---

## Violation

```python id="exc_bad"
class FileReader:
    def read(self):
        pass


class SafeFileReader(FileReader):
    def read(self):
        raise Exception("Something went wrong")  # too broad
```

### Problem

* Caller expects predictable behavior
* Child introduces unexpected failure

---

## Correct Approach

```python id="exc_good"
class FileNotFoundError(Exception):
    pass


class SafeFileReader(FileReader):
    def read(self):
        raise FileNotFoundError("File missing")  # specific
```

---

## Insight

> Exceptions should be **same or more specific**, never broader

---

# 4. Combined View

| Rule       | Allowed Change            | Not Allowed                   |
| ---------- | ------------------------- | ----------------------------- |
| Arguments  | Same or more general      | Narrower input types          |
| Return     | More specific (covariant) | More generic                  |
| Exceptions | Same or more specific     | Broader/unexpected exceptions |

---

# 5. Mental Model

Think in terms of **guarantees**:

* Arguments → what inputs are accepted
* Return → what output is promised
* Exceptions → what failures are expected

Child class must **not weaken these guarantees**

---

# 6. Practical System Insight

In real systems (APIs, services, LLM pipelines):

* Changing input expectations breaks clients
* Returning unexpected types breaks integrations
* Throwing new exceptions breaks reliability

---

# 7. Summary (Keep This Mental Model)

| Rule       | What NOT to do           |
| ---------- | ------------------------ |
| Arguments  | Narrow inputs            |
| Return     | Return more generic      |
| Exceptions | Throw broader/unexpected |

---

# Final Takeaway

> Subclasses should **extend behavior without weakening contracts**

That is how LSP is preserved in real systems.
