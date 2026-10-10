1. Principle of Least Knowledge (Law of Demeter)
Core idea
A method should only talk to:
1. Itself (self)
2. Objects passed as parameters
3. Objects it creates
4. Its direct attributes (HAS-A relationship)
In simple terms
“Don’t reach through objects to talk to strangers.”

2. Why this exists (real engineering motivation)
Without this rule, you get:
- deep coupling
- fragile chains
- cascading changes
- impossible refactoring
Classic symptom
user.getProfile().getAddress().getCity()


This looks harmless.
But it means:
- User depends on Profile
- Profile depends on Address
- Client depends on entire object graph
3. Naive Example (BAD DESIGN)
Let’s model a simple system:
- Order → User → Address → City
Classes
class Address:    def get_city(self):        return "Hyderabad"class Profile:    def __init__(self):        self.address = Address()    def get_address(self):        return self.addressclass User:    def __init__(self):        self.profile = Profile()    def get_profile(self):        return self.profileclass Order:    def __init__(self):        self.user = User()    def print_city(self):        city = self.user.get_profile().get_address().get_city()        print("Deliver to:", city)


Client
order = Order()order.print_city()


4. What is wrong here?
This violates the principle heavily.
Problem 1: Train-wreck coupling
order → user → profile → address → city


If ANY link changes:
- rename method
- restructure object
- split profile service
👉 Order.print_city() breaks
Problem 2: Ripple effect of change
If we change:
Profile → removes Address


You must update:
- Order
- every caller
Problem 3: “Knowledge leakage”
Order knows too much:
- internal structure of User
- internal structure of Profile
- internal structure of Address
5. Correct Design (Applying Principle)
We move responsibility downward.
Fix: Tell, don’t ask
Instead of:
“give me city step by step”

We do:
“User, tell me your city”

Step 1: Fix Address
class Address:    def get_city(self):        return "Hyderabad"


Step 2: Profile exposes behavior, not structure
class Profile:    def __init__(self):        self.address = Address()    def get_city(self):        return self.address.get_city()


Step 3: User hides internal chain
class User:
    def __init__(self):
        self.profile = Profile()

    def get_city(self):
        return self.profile.get_city()

Step 4: Order becomes clean
class Order:
    def __init__(self):
        self.user = User()

    def print_city(self):
        city = self.user.get_city()
        print("Deliver to:", city)

6. What changed?
Before
order.user.profile.address.city

Order knows entire object graph.
After
order.user.get_city()


Order knows only ONE abstraction.
7. Mapping to the RULES you gave
Let’s connect directly:
Rule 1: Only call methods on self
✔ Order uses only its own method print_city
Rule 2: Objects passed in parameters
Example:
def process(order):    order.get_city()


✔ allowed
Rule 3: Objects created inside method
def create():    u = User()    u.get_city()


✔ allowed
Rule 4: HAS-A relationships (direct, not deep)
Allowed:
self.user.get_city()


❌ NOT allowed:
self.user.profile.address.city


8. Real system design intuition (VERY IMPORTANT)
This principle is basically:
“Avoid deep object traversal in distributed thinking too”

Bad microservice design equivalent
OrderService → UserService → ProfileService → AddressService → DB

This creates:
- tight coupling across services
- cascading latency
- failure propagation chain
Good design
OrderService → UserService (getCity())

UserService hides internal service graph.
9. Why this matters for RAG systems (your domain)
Bad RAG:
query → embedder.embedder_model.tokenizer.cleaner.normalize()

Good RAG:
rag.query()


Internals hidden inside Facade.
So:
- Facade pattern = structural hiding
- Law of Demeter = interaction restriction
They complement each other.
10. When this rule is violated in real systems
You will see:
1. “God traversal code”
- long chained calls
- fragile pipelines
2. High refactor cost
- small internal change breaks everything
3. Testing difficulty
- mocks become complex
- deep dependency graphs
11. Trade-off (important honesty)
Sometimes violating it is intentional:
Acceptable violations:
- DTO objects
- data pipelines (pure transformations)
- performance-critical code (avoid wrapper layers)
But in most business logic:
follow it strictly

12. Final mental model
If you remember only this:
“A class should talk to friends, not strangers of friends.”