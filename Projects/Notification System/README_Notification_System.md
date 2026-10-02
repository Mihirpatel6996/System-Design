# Notification System — Dependency-First Design Notes

This README converts the UML design into a readable, implementation-oriented form.

The ordering is intentionally **dependency-first**: a class is introduced only after the classes/interfaces it directly depends on have already been explained.

---

# 1. System Requirements

The notification system must support four main requirements:

1. **Plug-and-play model**
   - New notification channels should be attachable without rewriting the core notification engine.

2. **Extensibility**
   - The system should support channels such as:
     - SMS
     - Email
     - Popup
   - More channels should be addable later.

3. **Dynamic notification changes**
   - The notification behavior/channel should be changeable at runtime rather than hard-coded permanently.

4. **Store and log notifications**
   - Notifications should be retained by the notification service.
   - A logger should receive notification updates and record them.

---

# 2. Design Patterns Used

The UML combines four patterns:

| Pattern | Main classes | Why it is used |
|---|---|---|
| **Decorator** | `Notification`, `NotificationDecorator`, `TimestampDecorator`, `SignatureDecorator` | Add extra notification content/behavior without modifying the original notification class |
| **Observer** | `NotificationObservable`, `NotificationObserver`, `Logger`, `NotificationEngine` | Automatically notify multiple interested objects when a notification changes |
| **Strategy** | `NotificationStrategy`, `EmailStrategy`, `SMSStrategy`, `PopupStrategy`, `NotificationEngine` | Change the delivery mechanism at runtime |
| **Singleton** | `NotificationService` | Provide one shared notification service/history |

The important idea is that the patterns are not isolated. They work together:

```text
Notification
    |
    | Decorator
    v
Decorated Notification
    |
    | becomes/current notification
    v
NotificationObservable
    |
    | Observer notification
    +--------------------+
    |                    |
    v                    v
Logger          NotificationEngine
                         |
                         | Strategy
              +----------+----------+
              |          |          |
              v          v          v
            Email       SMS       Popup
```

---

# 3. Dependency-First Construction Order

Build/read the system in this order:

```text
1. Notification
2. SimpleNotification
3. NotificationDecorator
4. TimestampDecorator
5. SignatureDecorator
6. NotificationObserver
7. NotificationObservable
8. Logger
9. NotificationStrategy
10. EmailStrategy
11. SMSStrategy
12. PopupStrategy
13. NotificationEngine
14. NotificationService
```

Why this order?

- `SimpleNotification` needs `Notification`.
- Decorators need `Notification`.
- `TimestampDecorator` and `SignatureDecorator` need `NotificationDecorator`.
- `NotificationObservable` needs `NotificationObserver` and `Notification`.
- `Logger` needs `NotificationObserver` and a reference to `NotificationObservable`.
- Concrete strategies need `NotificationStrategy`.
- `NotificationEngine` combines Observer + Strategy, so it must come after both abstractions.
- `NotificationService` is the high-level service that sits on top of the notification model.

---

# 4. Core Notification Abstraction

## 4.1 `Notification`

```text
<<abstract>>
Notification
-------------------------
+ getContent() : String
```

### Responsibility

`Notification` represents the basic concept of a notification.

It does not decide:

- how the notification is sent,
- where it is sent,
- whether it is logged,
- whether it has a timestamp,
- whether it has a signature.

It only defines the common contract:

> Any notification must be able to provide its content.

### Why abstract?

We usually do not want to create a generic `Notification` object directly.

Instead, concrete classes provide the actual notification content.

### Relationship

Other classes can have an **is-a** relationship with `Notification`.

```text
SimpleNotification IS-A Notification
NotificationDecorator IS-A Notification
```

This is **inheritance/generalization**.

---

# 5. Basic Concrete Notification

## 5.1 `SimpleNotification`

```text
SimpleNotification
-------------------------
- text : String
+ getContent() : String
```

### Dependency

```text
SimpleNotification
        |
        v
Notification
```

`SimpleNotification` must be introduced after `Notification` because it implements the `Notification` abstraction.

### Responsibility

It stores the original/plain notification text.

Example:

```text
SimpleNotification("Order has been delivered")
```

Possible content:

```text
"Order has been delivered"
```

### Relationship

```text
SimpleNotification --|> Notification
```

This is **is-a / inheritance**.

`SimpleNotification` is a kind of `Notification`.

### Why inheritance is appropriate

Anything that expects a `Notification` can receive a `SimpleNotification`.

For example:

```text
Notification n = new SimpleNotification("Hello");
```

---

# 6. Notification Decorator Abstraction

## 6.1 `NotificationDecorator`

```text
<<abstract>>
NotificationDecorator
-------------------------
- notif : Notification
+ getContent() : String
```

### Dependency

```text
NotificationDecorator
        |
        +----> Notification
```

The decorator itself is also a `Notification`.

```text
NotificationDecorator IS-A Notification
```

At the same time it **contains/references another Notification**:

```text
NotificationDecorator HAS-A Notification
```

This dual relationship is the key idea of the Decorator Pattern.

### Why both is-a and has-a?

Because a decorator must be usable everywhere a normal notification is expected, while also wrapping another notification.

Example:

```text
Notification
    ^
    |
NotificationDecorator
    |
    +---- wraps ----> Notification
```

### What should `notif` mean?

`notif` is the notification being decorated.

Example conceptually:

```text
TimestampDecorator
        wraps
SimpleNotification
```

### Association vs composition here

In the UML shown, the relationship behaves like a **reference/association** rather than composition.

Reason:

- The decorator needs another notification.
- The wrapped notification can conceptually exist independently.
- A pointer/reference is shown.

Therefore:

```text
Decorator ----> Notification
```

is best understood as an **association** unless your implementation explicitly makes the decorator responsible for the wrapped object's lifetime.

Do not automatically call this composition just because one object is stored inside another object.

---

# 7. Concrete Decorators

## 7.1 `TimestampDecorator`

```text
TimestampDecorator
-------------------------
- notif : Notification
+ getContent() : String
```

### Dependencies

```text
TimestampDecorator
        |
        v
NotificationDecorator
        |
        v
Notification
```

### Relationship

```text
TimestampDecorator --|> NotificationDecorator
```

This is **is-a / inheritance**.

And through the parent decorator it also wraps a `Notification`.

### Responsibility

Adds timestamp-related content without modifying the wrapped notification class.

Conceptual result:

```text
Original:
"Order delivered"

After TimestampDecorator:
"[10:30 PM] Order delivered"
```

The exact formatting is an implementation decision.

---

## 7.2 `SignatureDecorator`

```text
SignatureDecorator
-------------------------
- notif : Notification
+ getContent() : String
```

### Relationship

```text
SignatureDecorator --|> NotificationDecorator
```

Again, this is **is-a / inheritance**.

It wraps another notification and adds signature-related information.

Example conceptually:

```text
"Order delivered"
        |
        v
"Order delivered - Team Tomato"
```

---

# 8. Observer Abstraction

## 8.1 `NotificationObserver`

```text
<<abstract>>
NotificationObserver
-------------------------
+ update()
```

### Responsibility

This is the observer contract.

Any class that wants to receive notification-change events implements `update()`.

### Important relationship

```text
Logger --|> NotificationObserver
NotificationEngine --|> NotificationObserver
```

Both are **is-a / inheritance** relationships.

A `Logger` is an observer.
A `NotificationEngine` is also an observer.

### Why abstract?

Because the system cares about the behavior:

```text
update()
```

not the exact type of observer.

This allows more observers to be added later:

```text
AnalyticsObserver
AuditObserver
MetricsObserver
```

without changing the subject's basic notification mechanism.

---

# 9. Observer Subject

## 9.1 `NotificationObservable`

```text
NotificationObservable
-------------------------
- notif : Notification
- observers : List<NotificationObserver>

+ add(observer : NotificationObserver)
+ remove(observer : NotificationObserver)
+ notify()
+ setNotification(notification : Notification)
```

### Dependencies

It depends on:

```text
NotificationObservable
    |
    +----> Notification
    |
    +----> NotificationObserver
```

Therefore it appears after both abstractions in the dependency-first order.

### Responsibility

This is the **Subject** of the Observer Pattern.

It maintains:

1. the current notification,
2. a collection of observers.

Its main job is:

```text
setNotification(...)
        |
        v
      notify()
        |
        +----> Logger.update()
        |
        +----> NotificationEngine.update()
```

### Relationship with observers

```text
NotificationObservable
        |
        | 1..*
        v
NotificationObserver
```

The system allows one observable to have multiple observers.

### Association or aggregation?

The diagram shows a collection/reference relationship rather than explicit ownership.

Conceptually this is best treated as:

- **association** if you want to describe only that the subject knows about observers;
- **aggregation** if you want to explicitly say “the subject groups multiple independently existing observers.”

It is **not composition** because observers such as `Logger` can exist independently of the observable.

So the safest learning interpretation for this design is:

```text
NotificationObservable HAS-A collection of NotificationObserver references.
```

with **association/aggregation semantics**, not ownership.

---

# 10. Logger Observer

## 10.1 `Logger`

```text
Logger
-------------------------
- notificationObservable : NotificationObservable
+ update()
```

### Dependencies

```text
Logger
  |
  +----> NotificationObserver
  |
  +----> NotificationObservable
```

### Relationship 1 — Observer

```text
Logger --|> NotificationObserver
```

This is **is-a / inheritance**.

### Relationship 2 — Observable reference

```text
Logger ----> NotificationObservable
```

This is an **association**.

Why?

`Logger` needs to know which observable it is associated with so that its `update()` operation can access the relevant notification/state.

The observable does not become a part of the logger's identity, and the logger does not own the observable.

Therefore it should not be modeled as composition.

### Responsibility

Whenever the subject changes and calls `notify()`:

```text
NotificationObservable
        |
        v
Logger.update()
```

The logger stores or records the notification.

---

# 11. Notification Delivery Strategy

## 11.1 `NotificationStrategy`

```text
<<abstract>>
NotificationStrategy
-------------------------
+ sendNotification(contents : String)
```

### Responsibility

This is the Strategy Pattern interface.

It represents a **way to deliver a notification**.

The interface does not care whether delivery uses:

- email,
- SMS,
- popup,
- or a future channel.

### Important distinction

`Notification` describes **what the notification is**.

`NotificationStrategy` describes **how the notification is delivered**.

That separation is extremely important.

---

# 12. Concrete Strategies

## 12.1 `EmailStrategy`

```text
EmailStrategy
-------------------------
+ sendNotification(contents : String)
```

```text
EmailStrategy --|> NotificationStrategy
```

This is **is-a / inheritance**.

It implements email delivery.

---

## 12.2 `SMSStrategy`

```text
SMSStrategy
-------------------------
+ sendNotification(contents : String)
```

```text
SMSStrategy --|> NotificationStrategy
```

This is **is-a / inheritance**.

It implements SMS delivery.

---

## 12.3 `PopupStrategy`

```text
PopupStrategy
-------------------------
+ sendNotification(contents : String)
```

```text
PopupStrategy --|> NotificationStrategy
```

This is **is-a / inheritance**.

It implements popup delivery.

---

# 13. Notification Engine

## 13.1 `NotificationEngine`

```text
NotificationEngine
-------------------------
- notificationObservable : NotificationObservable
- strategies : List<NotificationStrategy>
+ update()
```

### Dependencies

This class is introduced late because it combines both major abstractions:

```text
NotificationEngine
      |
      +----> NotificationObserver
      |
      +----> NotificationObservable
      |
      +----> NotificationStrategy
```

### Relationship 1 — Observer

```text
NotificationEngine --|> NotificationObserver
```

This is **is-a / inheritance**.

The engine is an observer because it must react when a notification changes.

### Relationship 2 — Observable

```text
NotificationEngine ----> NotificationObservable
```

This is an **association**.

The engine needs access to the observable/notification state but does not own it.

### Relationship 3 — Strategies

```text
NotificationEngine
        |
        |  has a collection of strategies
        v
NotificationStrategy
```

This is a **has-a relationship**.

Conceptually it is association/aggregation rather than composition when strategies are created and managed independently.

For example:

```text
EmailStrategy
SMSStrategy
PopupStrategy
```

can exist independently of the engine.

### Responsibility

`NotificationEngine` is the bridge between Observer and Strategy.

Flow:

```text
Notification changes
        |
        v
NotificationObservable.notify()
        |
        v
NotificationEngine.update()
        |
        v
Choose appropriate strategy
        |
        v
strategy.sendNotification(content)
```

This is where the two patterns cooperate.

---

# 14. Notification Service

## 14.1 `NotificationService`

```text
<<Singleton>>
NotificationService
-------------------------
- notifications : List<Notification>
+ sendNotification(...)
```

### Pattern

This class uses the **Singleton Pattern**.

The `<<Singleton>>` label means the design intends there to be one globally shared instance of the service.

### Responsibility

The service acts as the central notification service/history holder.

It can be responsible for:

- accepting notifications,
- storing notification history,
- coordinating notification processing.

### Relationship with `Notification`

```text
NotificationService
        |
        | 1..*
        v
Notification
```

The service maintains multiple notifications.

This is a **has-a** relationship.

However, the exact UML ownership semantics depend on how the collection is implemented.

### Important modeling detail

If the implementation literally uses:

```text
List<Notification>
```

and `Notification` is abstract, you cannot normally instantiate `Notification` directly.

A more implementation-friendly representation is often something like:

```text
List<Notification>      // language-dependent / value semantics
```

or

```text
List<Notification*>     // pointer/reference-based design
```

or

```text
List<Notification>      // using a language that supports interface/reference collections
```

depending on the programming language.

The UML idea is simply:

> NotificationService keeps a collection of notification objects/history.

### Singleton is not a relationship

`<<Singleton>>` should not be confused with:

- association,
- aggregation,
- composition,
- inheritance.

It describes the **creation/lifecycle policy of the class**, not how it is related to another class.

---

# 15. Complete Class Structure

```text
                           <<abstract>>
                          Notification
                          + getContent()
                              ^
                    +---------+---------+
                    |                   |
                    |                   |
          SimpleNotification   <<abstract>> NotificationDecorator
                               - notif : Notification
                               + getContent()
                                      ^
                              +-------+-------+
                              |               |
                     TimestampDecorator  SignatureDecorator
```

Observer side:

```text
                    <<abstract>>
                 NotificationObserver
                      + update()
                          ^
                          |
               +----------+-----------+
               |                      |
             Logger          NotificationEngine
               |                      |
               |                      +----> NotificationObservable
               |                      |
               +----> NotificationObservable
                                      |
                                      | 1..*
                                      v
                             NotificationObserver
```

Strategy side:

```text
                    <<abstract>>
                 NotificationStrategy
               + sendNotification(...)
                         ^
            +------------+------------+
            |            |            |
          Email          SMS         Popup
         Strategy      Strategy      Strategy
```

Singleton/history side:

```text
              <<Singleton>>
            NotificationService
             - notifications
             + sendNotification()
                    |
                    | 1..*
                    v
               Notification
```

---

# 16. Full Dependency Graph

This is the most useful graph for implementing the project from the bottom upward:

```text
Notification
    |
    +--------------------------+
    |                          |
    v                          v
SimpleNotification      NotificationDecorator
                               |
                      +--------+--------+
                      |                 |
                      v                 v
             TimestampDecorator   SignatureDecorator

NotificationObserver
    |
    +----------------------+ 
    |                      |
    v                      v
  Logger          NotificationEngine
    |                      |
    |                      +--------------------+
    |                      |                    |
    v                      v                    v
NotificationObservable  NotificationStrategy   observers/subject refs
                           |
                 +---------+---------+
                 |         |         |
                 v         v         v
               Email      SMS      Popup
```

A cleaner implementation dependency chain is:

```text
Notification
   ↓
SimpleNotification
   ↓
NotificationDecorator
   ↓
TimestampDecorator / SignatureDecorator

NotificationObserver
   ↓
NotificationObservable
   ↓
Logger

NotificationStrategy
   ↓
EmailStrategy / SMSStrategy / PopupStrategy
   ↓
NotificationEngine
   ↓
NotificationService
```

Note that some classes are actually independent until the higher-level classes combine them. Therefore, “dependency-first” is better understood as a **topological order**, not necessarily one single straight inheritance tree.

---

# 17. Relationship Cheat Sheet

This section is important for learning UML rather than merely memorizing the final diagram.

## 17.1 IS-A

Means inheritance/generalization.

Examples:

```text
SimpleNotification IS-A Notification
NotificationDecorator IS-A Notification
TimestampDecorator IS-A NotificationDecorator
SignatureDecorator IS-A NotificationDecorator
Logger IS-A NotificationObserver
NotificationEngine IS-A NotificationObserver
EmailStrategy IS-A NotificationStrategy
SMSStrategy IS-A NotificationStrategy
PopupStrategy IS-A NotificationStrategy
```

UML notation:

```text
Child --------|> Parent
```

The hollow triangle points toward the parent.

---

## 17.2 HAS-A

Means one object keeps or uses another object/reference.

Examples:

```text
NotificationDecorator HAS-A Notification
NotificationObservable HAS-A Notification
NotificationObservable HAS-A many NotificationObservers
Logger HAS-A/knows NotificationObservable
NotificationEngine HAS-A/knows NotificationObservable
NotificationEngine HAS-A strategies
NotificationService HAS-A notifications
```

But **HAS-A is not a single UML relationship type**.

It can be represented by different UML relationships depending on ownership and lifecycle.

---

# 18. Association vs Aggregation vs Composition

This is where beginners often make mistakes.

## 18.1 Association

Association means:

> Object A knows about or uses Object B.

The objects can usually exist independently.

Examples in this system:

```text
Logger ----> NotificationObservable
NotificationEngine ----> NotificationObservable
```

Reason:

- Logger does not own the observable.
- Engine does not own the observable.
- The observable can exist without either one.

---

## 18.2 Aggregation

Aggregation means:

> Object A groups objects B, but B can still live independently.

Example conceptually:

```text
NotificationObservable o----> NotificationObserver
```

The observable has a collection of observers, but the observers do not depend on the observable for their entire lifetime.

Similarly:

```text
NotificationEngine o----> NotificationStrategy
```

can be viewed as aggregation when the engine groups independently existing strategies.

Important:

**Aggregation should only be used when the “whole-part” meaning is actually useful.**

A collection alone does not automatically mean aggregation.

---

## 18.3 Composition

Composition means:

> Object A owns object B strongly, and B's lifetime is tied to A.

Example of composition in general:

```text
House *---- Room
```

If the house is destroyed, the room as a modeled part is destroyed with it.

### In this notification design

The important relationships are mostly **not composition**.

Why?

Because:

- `Logger` should exist independently.
- `NotificationEngine` should exist independently.
- Strategies should be replaceable and can exist independently.
- The wrapped `Notification` may exist independently of a decorator.

Therefore, do not mark all “member variables” as composition.

---

# 19. Why Decorator + Strategy + Observer Work Together

The patterns solve different problems.

## Decorator solves:

> “How do I add optional features to a notification without creating many subclasses?”

Example:

```text
SimpleNotification
        |
        v
TimestampDecorator
        |
        v
SignatureDecorator
```

Result:

```text
base content
   + timestamp
   + signature
```

---

## Observer solves:

> “How do multiple components automatically react when a notification changes?”

Example:

```text
NotificationObservable
        |
        +----> Logger
        |
        +----> NotificationEngine
```

---

## Strategy solves:

> “How do I change the delivery algorithm/channel without changing the engine?”

Example:

```text
NotificationEngine
        |
        +----> EmailStrategy
        +----> SMSStrategy
        +----> PopupStrategy
```

The engine can choose a strategy at runtime.

---

## Singleton solves:

> “How do I make the central notification service globally shared?”

Example:

```text
NotificationService.getInstance()
```

The exact API depends on the programming language.

---

# 20. End-to-End Runtime Flow

A typical flow based on the UML is:

```text
1. Create a basic notification

   SimpleNotification
          |
          v
   "Order delivered"

2. Add optional information using decorators

   TimestampDecorator
          |
          v
   SignatureDecorator
          |
          v
   Decorated Notification

3. Store/process the notification

   NotificationService

4. Set the current notification in the subject

   NotificationObservable.setNotification(notification)

5. Notify observers

   NotificationObservable.notify()
          |
          +------------------+
          |                  |
          v                  v
       Logger       NotificationEngine
                         |
                         v
                  choose strategy
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Email            SMS           Popup
```

---

# 21. How Each Requirement Is Supported

## Requirement 1 — Plug-and-play

The Strategy interface provides a common delivery contract.

```text
NotificationStrategy
        |
        +---- EmailStrategy
        +---- SMSStrategy
        +---- PopupStrategy
```

A new channel can be added as another implementation.

Example:

```text
PushStrategy --|> NotificationStrategy
```

The existing strategy abstraction remains unchanged.

---

## Requirement 2 — Extensible notification channels

The Strategy Pattern makes each channel a separate class.

Instead of:

```text
if type == SMS
else if type == EMAIL
else if type == POPUP
```

being spread throughout the code, the delivery behavior is encapsulated inside strategy classes.

---

## Requirement 3 — Dynamic change

The engine can work against the abstraction:

```text
NotificationStrategy
```

instead of hard-coding a concrete implementation.

Conceptually:

```text
engine.setStrategy(emailStrategy)

...later...

engine.setStrategy(smsStrategy)
```

The exact `setStrategy()` method is not explicitly shown in the UML, so it would need to be added if this is a required runtime API.

---

## Requirement 4 — Store and log notifications

Two responsibilities are separated:

```text
NotificationService
    -> stores notification history

Logger
    -> observes notification changes and logs them
```

This separation is useful because storing the application-level notification history and logging/auditing are not necessarily the same concern.

---

# 22. Important Design Improvements to Consider

The UML is a good learning model, but there are several places where you should make the responsibility boundaries explicit in code.

## 22.1 Add an explicit strategy setter if dynamic switching is required

The requirement says strategies can change dynamically.

The diagram currently shows the engine holding strategies, but not an explicit operation such as:

```text
setStrategy(strategy : NotificationStrategy)
```

Without such a mechanism, runtime strategy switching is not obvious from the UML.

A cleaner Strategy-based design is often:

```text
NotificationEngine
-------------------------
- strategy : NotificationStrategy
+ setStrategy(strategy : NotificationStrategy)
+ update()
```

If you intentionally want multiple registered strategies, then keeping a collection is reasonable, but you still need a selection rule.

---

## 22.2 Clarify the responsibility of `NotificationService.sendNotification()`

There are two possible responsibilities in the current model:

```text
NotificationService.sendNotification()
```

and

```text
NotificationEngine.update()
    -> strategy.sendNotification()
```

That can create overlapping responsibilities.

A cleaner separation would be:

```text
NotificationService
    = facade/orchestrator + history

NotificationObservable
    = event source

NotificationEngine
    = delivery decision/routing

NotificationStrategy
    = actual delivery mechanism

Logger
    = logging/auditing
```

This makes each class easier to reason about.

---

## 22.3 Decide whether the service stores objects or notification records

If `NotificationService` is mainly for history, you may eventually prefer something like:

```text
NotificationRecord
-------------------------
notificationId
content
timestamp
channel
status
```

rather than storing the same live notification object graph forever.

That is not required for the learning version, but it becomes relevant in a production system.

---

## 22.4 Consider passing the changed notification to `update()`

The diagram currently has:

```text
update()
```

with no argument.

Another common design is:

```text
update(notification : Notification)
```

This reduces the need for the observer to ask the observable for state.

Both designs are possible.

The current UML specifically suggests that observers keep a reference to the observable and obtain the relevant state from there.

---

# 23. Learning the Diagram Through Questions

When you see a relationship, ask these questions in order.

### Question 1 — Is this an IS-A relationship?

Ask:

> Is class A a specialized kind of class B?

If yes:

```text
A --|> B
```

Example:

```text
EmailStrategy --|> NotificationStrategy
```

---

### Question 2 — Does A merely know/use B?

If yes, use **association**.

Example:

```text
Logger ----> NotificationObservable
```

---

### Question 3 — Does A group independent B objects?

If yes, **aggregation** may communicate that whole-part relationship.

Example:

```text
NotificationObservable o----> NotificationObserver
```

---

### Question 4 — Does A own B's lifetime?

If yes, **composition** may be appropriate.

Example in this system only if you deliberately make the lifecycle dependent.

Do not use composition merely because B is a member variable.

---

# 24. Final UML in Readable Text Form

```text
============================================================
NOTIFICATION MODEL / DECORATOR
============================================================

<<abstract>>
Notification
------------------------------------------------------------
+ getContent() : String

SimpleNotification --|> Notification
SimpleNotification
------------------------------------------------------------
- text : String
+ getContent() : String

<<abstract>>
NotificationDecorator --|> Notification
------------------------------------------------------------
- notif : Notification
+ getContent() : String

TimestampDecorator --|> NotificationDecorator
------------------------------------------------------------
- notif : Notification
+ getContent() : String

SignatureDecorator --|> NotificationDecorator
------------------------------------------------------------
- notif : Notification
+ getContent() : String


============================================================
OBSERVER
============================================================

<<abstract>>
NotificationObserver
------------------------------------------------------------
+ update()

NotificationObservable
------------------------------------------------------------
- notif : Notification
- observers : List<NotificationObserver>
+ add(observer : NotificationObserver)
+ remove(observer : NotificationObserver)
+ notify()
+ setNotification(notification : Notification)

NotificationObservable ----> NotificationObserver (1..*)

Logger --|> NotificationObserver
Logger
------------------------------------------------------------
- notificationObservable : NotificationObservable
+ update()

Logger ----> NotificationObservable

NotificationEngine --|> NotificationObserver


============================================================
STRATEGY
============================================================

<<abstract>>
NotificationStrategy
------------------------------------------------------------
+ sendNotification(contents : String)

EmailStrategy --|> NotificationStrategy
------------------------------------------------------------
+ sendNotification(contents : String)

SMSStrategy --|> NotificationStrategy
------------------------------------------------------------
+ sendNotification(contents : String)

PopupStrategy --|> NotificationStrategy
------------------------------------------------------------
+ sendNotification(contents : String)


============================================================
ENGINE
============================================================

NotificationEngine
------------------------------------------------------------
- notificationObservable : NotificationObservable
- strategies : List<NotificationStrategy>
+ update()

Relationships:
NotificationEngine --|> NotificationObserver
NotificationEngine ----> NotificationObservable
NotificationEngine ----> NotificationStrategy (collection)


============================================================
SERVICE / SINGLETON
============================================================

<<Singleton>>
NotificationService
------------------------------------------------------------
- notifications : List<Notification>
+ sendNotification(...)

NotificationService ----> Notification (1..*)
```

---

# 25. Mental Model of the Whole System

Think of the design as five layers of responsibility:

```text
                    NOTIFICATION CONTENT
                             |
                             v
                    Notification
                             |
                             v
                         Decorator
                             |
                             v
                   Final notification content
                             |
                             v
                    Observable / Subject
                       /             \
                      /               \
                     v                 v
                  Logger        NotificationEngine
                                       |
                                       v
                                  Strategy
                              /       |       \
                             v        v        v
                           Email     SMS      Popup

                    NotificationService
                    = central service/history
                    = Singleton access point
```

The core separation is:

```text
WHAT is the notification?
    -> Notification

HOW is the notification enhanced?
    -> Decorator

WHO should react when it changes?
    -> Observer

HOW should it be delivered?
    -> Strategy

WHERE is the central service/history?
    -> Singleton NotificationService
```

That is the main architectural idea behind the UML.

---

# 26. One-Line Relationship Summary

```text
SimpleNotification IS-A Notification

NotificationDecorator IS-A Notification
NotificationDecorator HAS-A Notification

TimestampDecorator IS-A NotificationDecorator
SignatureDecorator IS-A NotificationDecorator

Logger IS-A NotificationObserver
Logger ASSOCIATES WITH NotificationObservable

NotificationObservable HAS-A Notification
NotificationObservable HAS-A collection of NotificationObservers

NotificationEngine IS-A NotificationObserver
NotificationEngine ASSOCIATES WITH NotificationObservable
NotificationEngine HAS-A collection of NotificationStrategies

EmailStrategy IS-A NotificationStrategy
SMSStrategy IS-A NotificationStrategy
PopupStrategy IS-A NotificationStrategy

NotificationService HAS-A collection of Notifications
NotificationService IS-A Singleton by design policy, not by inheritance
```

The important lesson is:

> **“Has-a” is a conceptual description, while association, aggregation, and composition describe different UML semantics for that relationship.**

Do not use aggregation or composition automatically. Decide based on **knowledge, ownership, lifecycle, and independence of the objects**.
