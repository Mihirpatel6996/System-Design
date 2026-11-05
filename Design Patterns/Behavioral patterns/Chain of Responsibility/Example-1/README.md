1. What problem are we solving?
Think like a system designer first.
You have an ATM:
- It has ₹1000, ₹500, ₹200, ₹100 notes
- User asks: “Give me ₹3700”
- ATM should:
  - Try ₹1000 notes first
  - Then ₹500
  - Then ₹200
  - Then ₹100
Now here’s the key design question:
Who decides how to split the amount?

Naive answer:
One big function that knows everything.
Better answer:
Each denomination should handle its part and pass the rest.
That’s where Chain of Responsibility comes in.
2. Definition (clear, not textbook)
Chain of Responsibility = pass a request through a chain of handlers, where each handler:
- processes what it can
- forwards the remaining work to the next handler
Mental model
Request → Handler1 → Handler2 → Handler3 → Handler4
             ↓           ↓           ↓
        handles part  handles part  handles part

Each handler:
- does partial work
- does NOT know full system
- only knows: “if I can’t fully handle → pass forward”
3. Naive Implementation (Python)
Let’s first NOT use the pattern.
We centralize logic in one class.
class ATM:    def __init__(self):        self.notes = {            1000: 3,            500: 5,            200: 10,            100: 20        }    def dispense(self, amount):        print(f"\nDispensing amount: ₹{amount}")        for denom in [1000, 500, 200, 100]:            if amount <= 0:                break            available = self.notes[denom]            needed = amount // denom            used = min(needed, available)            if used > 0:                print(f"Dispensing {used} x ₹{denom}")                self.notes[denom] -= used                amount -= used * denom        if amount > 0:            print(f"Remaining ₹{amount} cannot be dispensed")


Usage
atm = ATM()atm.dispense(3700)


4. Why this breaks (important)
This works… but from a system design POV, it’s bad.
Problem 1: Tight coupling
- ATM knows ALL denominations
- Adding ₹50 note → modify this class
Problem 2: Violates Open/Closed Principle
Want to add ₹2000 notes?

You must edit dispense() logic.
Problem 3: No flexibility in ordering
What if RBI changes rule:
- dispense smaller notes first?
You rewrite logic.
Problem 4: No reuse
You cannot reuse ₹500 logic independently.
Problem 5: Hard to scale mentally
Imagine:
- currency conversion
- multi-country ATMs
- dynamic denominations
This single function becomes a nightmare.
5. Key insight (this is where pattern comes)
Look at the repeated logic:
needed = amount // denomused = min(needed, available)remaining = amount - used * denom


Every denomination:
- behaves SAME WAY
- only differs by:
  - denomination value
  - number of notes
So instead of:
One class handling everything

We want:
Each denomination becomes a handler


1. Core Idea Before Code
We are changing who controls the flow.
Naive:
ATM → loops → handles everything

Chain of Responsibility:
User → 1000Handler → 500Handler → 200Handler → 100Handler

Each handler:
- handles its denomination
- passes remaining amount forward
2. Base Handler (Abstraction)
This is your Java MoneyHandler.
class MoneyHandler:    def __init__(self):        self.next_handler = None    def set_next(self, handler):        self.next_handler = handler        return handler  # enables chaining    def dispense(self, amount):        raise NotImplementedError


Why this exists?
- Defines contract
- Holds reference to next handler
- Enables dynamic chain building
3. Concrete Handlers
Instead of repeating logic 4 times, we’ll slightly generalize.
But first, let’s mirror your Java style for clarity.
₹1000 Handler
class ThousandHandler(MoneyHandler):    def __init__(self, num_notes):        super().__init__()        self.num_notes = num_notes    def dispense(self, amount):        notes_needed = amount // 1000        if notes_needed > self.num_notes:            notes_to_use = self.num_notes            self.num_notes = 0        else:            notes_to_use = notes_needed            self.num_notes -= notes_to_use        if notes_to_use > 0:            print(f"Dispensing {notes_to_use} x ₹1000 notes")        remaining = amount - (notes_to_use * 1000)        if remaining > 0:            if self.next_handler:                self.next_handler.dispense(remaining)            else:                print(f"Remaining ₹{remaining} cannot be dispensed")


₹500 Handler
class FiveHundredHandler(MoneyHandler):    def __init__(self, num_notes):        super().__init__()        self.num_notes = num_notes    def dispense(self, amount):        notes_needed = amount // 500        if notes_needed > self.num_notes:            notes_to_use = self.num_notes            self.num_notes = 0        else:            notes_to_use = notes_needed            self.num_notes -= notes_to_use        if notes_to_use > 0:            print(f"Dispensing {notes_to_use} x ₹500 notes")        remaining = amount - (notes_to_use * 500)        if remaining > 0:            if self.next_handler:                self.next_handler.dispense(remaining)            else:                print(f"Remaining ₹{remaining} cannot be dispensed")


₹200 Handler
class TwoHundredHandler(MoneyHandler):    def __init__(self, num_notes):        super().__init__()        self.num_notes = num_notes    def dispense(self, amount):        notes_needed = amount // 200        if notes_needed > self.num_notes:            notes_to_use = self.num_notes            self.num_notes = 0        else:            notes_to_use = notes_needed            self.num_notes -= notes_to_use        if notes_to_use > 0:            print(f"Dispensing {notes_to_use} x ₹200 notes")        remaining = amount - (notes_to_use * 200)        if remaining > 0:            if self.next_handler:                self.next_handler.dispense(remaining)            else:                print(f"Remaining ₹{remaining} cannot be dispensed")


₹100 Handler
class HundredHandler(MoneyHandler):    def __init__(self, num_notes):        super().__init__()        self.num_notes = num_notes    def dispense(self, amount):        notes_needed = amount // 100        if notes_needed > self.num_notes:            notes_to_use = self.num_notes            self.num_notes = 0        else:            notes_to_use = notes_needed            self.num_notes -= notes_to_use        if notes_to_use > 0:            print(f"Dispensing {notes_to_use} x ₹100 notes")        remaining = amount - (notes_to_use * 100)        if remaining > 0:            if self.next_handler:                self.next_handler.dispense(remaining)            else:                print(f"Remaining ₹{remaining} cannot be dispensed")


4. Building the Chain
This is the most important part.
# Create handlersh1000 = ThousandHandler(3)h500 = FiveHundredHandler(5)h200 = TwoHundredHandler(10)h100 = HundredHandler(20)# Build chainh1000.set_next(h500).set_next(h200).set_next(h100)


What just happened?
This line:
h1000.set_next(h500).set_next(h200).set_next(h100)


creates:
1000 → 500 → 200 → 100

5. Running the System
amount = 3700print(f"\nDispensing ₹{amount}")h1000.dispense(amount)


6. Flow Trace (Important for intuition)
Let’s simulate:
Input: ₹3700
1000 handler:
  uses 3 notes → ₹3000
  remaining = ₹700 → pass

500 handler:
  uses 1 note → ₹500
  remaining = ₹200 → pass

200 handler:
  uses 1 note → ₹200
  remaining = ₹0 → stop

7. Why this is powerful
1. Loose coupling
- 1000 handler does NOT know about 500
- Only knows “next”
2. Extendable
Add ₹50:
h50 = FiftyHandler(30)h100.set_next(h50)


No existing code changed.
3. Reorder behavior dynamically
Want smallest notes first?
100 → 200 → 500 → 1000

Just change chain.
4. Partial handling (key idea)
Each handler:
- does what it can
- forwards rest
This is the essence.
8. Where people get confused (your point)
You said:
“somewhat related to Template Method”

You’re not wrong — but the difference is critical:
Template Method
- Flow is fixed in base class
- Steps are overridden
Base class controls algorithm

Chain of Responsibility
- Flow is dynamic at runtime
- Handlers decide whether to pass forward
No central controller

In ATM:
- Template → one class decides full flow
- Chain → flow emerges from linking handlers
9. Real System Mapping (important for you)
This pattern is heavily used in:
1. API Gateways / Middleware
Request → Auth → RateLimit → Logging → Handler

Each:
- processes
- forwards
2. LLM / RAG pipelines (your domain)
Query →
  Safety Filter →
  Query Rewriter →
  Retriever →
  Reranker →
  Generator

Each stage:
- may modify / reject / pass forward
3. Logging frameworks
DEBUG → INFO → WARN → ERROR

10. Limitations (don’t ignore this)
1. Debugging becomes harder
Flow is not centralized.
2. Performance
Multiple handlers = overhead.
Time complexity:
- Worst case: O(n handlers)
3. No guarantee someone handles request
You must design fallback.
11. Where this breaks at scale
Think:
What if ATM has dynamic denominations from DB?

- Chain must be built dynamically
- Might require factory + config-driven system
What if 1000 ATMs update state concurrently?

- You need:
  - central inventory store
  - locking / transactions
So pattern solves code structure, not distributed consistency.


Good catch — this one line looks simple but hides how the chain is actually constructed. Let’s trace it like a system, not just syntax.
1. The Code We’re Tracing
h1000.set_next(h500).set_next(h200).set_next(h100)


2. First, understand set_next
def set_next(self, handler):    self.next_handler = handler    return handler


Critical design decision:
It returns the handler you just passed.
That’s what enables chaining.
3. Step-by-Step Execution Trace
We evaluate left to right.
Step 1
h1000.set_next(h500)


What happens internally?
h1000.next_handler = h500return h500


Now:
h1000 → h500

And the expression returns h500
Step 2
Now the returned value (h500) continues:
(h500).set_next(h200)


Internally:
h500.next_handler = h200return h200


Now:
h1000 → h500 → h200

And expression returns h200
Step 3
Now:
(h200).set_next(h100)


Internally:
h200.next_handler = h100
return h100

Final chain:
h1000 → h500 → h200 → h100 → None

4. Final Memory State (Important)
Handler	next_handler
h1000	h500
h500	h200
h200	h100
h100	None


5. Visual Flow (Runtime)
When you call:
h1000.dispense(3700)


Flow becomes:
h1000
  ↓
h500
  ↓
h200
  ↓
h100

Each one:
- processes part
- forwards remainder
6. Why return handler (Design Insight)
If set_next didn’t return anything:
h1000.set_next(h500)h500.set_next(h200)h200.set_next(h100)


Same result — but more verbose.
With return → fluent API
h1000.set_next(h500).set_next(h200).set_next(h100)


This is called:
method chaining / fluent interface

Used in:
- query builders
- pipelines
- middleware configs
7. Subtle but Important System Insight
This line is not just syntax sugar.
It means:
The chain structure is built at runtime, not hardcoded.

Why that matters?
You can do:
if high_load:    h1000.set_next(h200).set_next(h100)else:    h1000.set_next(h500).set_next(h200).set_next(h100)


Dynamic behavior.
8. Failure Thinking (important)
What if you forget:
h200.set_next(h100)


Then:
h1000 → h500 → h200 → None

If amount remains after h200 → request dies silently
This is a real production risk in CoR systems:
- broken chain = lost processing
9. Compare with Real Systems
Think about your RAG pipeline:
Query → Safety → Rewrite → Retrieve → Generate

You can build it like:
safety.set_next(rewrite).set_next(retrieve).set_next(generate)


Now imagine:
- turning off rewrite
- inserting reranker dynamically
Same concept.
10. Final Check (your understanding)
Answer this:
If I change the chain to:

h100.set_next(h200).set_next(h500).set_next(h1000)


What happens to:
- output quality?
- number of notes dispensed?
This will tell me if you truly understood flow vs logic separation.