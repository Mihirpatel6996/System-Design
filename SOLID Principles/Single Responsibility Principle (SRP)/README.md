# S — Single Responsibility Principle (SRP)

---

# 1. Problem (Real System Context)

You are building a clinical AI pipeline:

```text id="flow1"
Kafka → Consumer → Process Vitals → Store → Generate Alert → Notify → Log
```

A naive approach is to put everything into a single class.

---

# 2. Naive Implementation (SRP Violation)

```python id="bad1"
class PatientMonitor:

    def __init__(self, db):
        self.db = db

    def consume_kafka(self, message):
        return message

    def process_vitals(self, data):
        hr = data["heart_rate"]
        if hr > 120:
            return "HIGH_RISK"
        return "NORMAL"

    def save_to_db(self, patient_id, status):
        print(f"Saving {patient_id} → {status}")

    def send_alert(self, patient_id, status):
        if status == "HIGH_RISK":
            print(f"ALERT sent for {patient_id}")

    def log(self, message):
        print(f"LOG: {message}")

    def run(self, message):
        data = self.consume_kafka(message)
        status = self.process_vitals(data)
        self.save_to_db(data["patient_id"], status)
        self.send_alert(data["patient_id"], status)
        self.log("Processed successfully")
```

---

# 3. Problem Analysis

This class handles:

* Kafka consumption
* Business logic
* Database storage
* Alerting
* Logging

### Consequences

* Any change impacts the same class
* Hard to test
* Hard to reuse
* High coupling

---

# 4. What SRP Actually Means

> A class should have **one reason to change**

Not “one method per class”
Not “make everything tiny”

---

## Identify Change Axes

| Responsibility    | Why it Changes               |
| ----------------- | ---------------------------- |
| Kafka consumption | Infrastructure changes       |
| Vitals processing | ML / business logic changes  |
| Storage           | DB / schema changes          |
| Alerting          | Notification channel changes |
| Logging           | Observability changes        |

Current design:

* 1 class
* 5 independent reasons to change

---

# 5. Refactor — Apply SRP

## Step 1: Split Responsibilities

```python id="comp1"
class KafkaConsumer:
    def consume(self, message):
        return message
```

```python id="comp2"
class VitalsProcessor:
    def process(self, data):
        hr = data["heart_rate"]
        return "HIGH_RISK" if hr > 120 else "NORMAL"
```

```python id="comp3"
class PatientRepository:
    def save(self, patient_id, status):
        print(f"Saving {patient_id} → {status}")
```

```python id="comp4"
class AlertService:
    def send(self, patient_id, status):
        if status == "HIGH_RISK":
            print(f"ALERT sent for {patient_id}")
```

```python id="comp5"
class Logger:
    def log(self, message):
        print(f"LOG: {message}")
```

---

## Step 2: Orchestrator

```python id="orchestrator"
class PatientMonitorService:

    def __init__(self, consumer, processor, repo, alert, logger):
        self.consumer = consumer
        self.processor = processor
        self.repo = repo
        self.alert = alert
        self.logger = logger

    def run(self, message):
        data = self.consumer.consume(message)
        status = self.processor.process(data)
        self.repo.save(data["patient_id"], status)
        self.alert.send(data["patient_id"], status)
        self.logger.log("Processed successfully")
```

---

# 6. What Changed

### Change alerting system

→ Modify only `AlertService`

### Switch database

→ Modify only `PatientRepository`

### Improve processing logic

→ Modify only `VitalsProcessor`

### Reuse logic in batch jobs

→ Use `VitalsProcessor` independently

---

# 7. System-Level Insight

SRP is not about classes.

> It is about **separating independent change vectors**

* If things change together → keep them together
* If they change independently → separate them

---

# 8. Trade-offs

## Benefits

* High maintainability
* Easy testing (mock dependencies)
* Replaceable components
* Clear ownership

---

## Costs

* More classes and files
* Requires discipline
* Can increase system complexity

---

# 9. When SRP Becomes a Problem

Overuse leads to:

* Too many small classes
* Complex dependency graphs
* Hard-to-follow execution flow

Example:

```text id="overkill"
PatientMonitorService → 15 dependencies
```

---

# 10. Scaling Perspective

## Small Scale

* SRP may feel unnecessary

## Medium Scale (team environment)

* Different modules owned by different developers

## Large Scale (production systems)

* Teams separated by responsibility
* SRP becomes essential

---

# 11. Common Mistakes

* Splitting trivial logic unnecessarily
* Premature abstraction
* Turning everything into microservices too early

---

# 12. Mental Model

When writing a class, ask:

* What are the reasons this code will change?
* Are those reasons independent?

If yes:

→ Split into separate components

---

# Final Insight

SRP is not about making code look clean.

> It is about making systems **change safely without breaking unrelated parts**
