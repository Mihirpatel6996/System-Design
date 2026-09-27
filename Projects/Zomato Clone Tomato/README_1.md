# Tomato — Zomato Clone: System Design Notes

A reference doc converting your hand-drawn UML into structured notes — classes, patterns, and **every relationship with the reasoning behind it**.

---

## 1. Requirements Recap

**Functional**

- User can search restaurants by location
- User can add items to a cart
- User can checkout by paying (via a 3rd-party payment method)
- User is notified once the order is placed

**Non-Functional**

- Scalable — adding new restaurants, payment methods, or order types shouldn't break existing code
- Modifiable — each concern (payment, order creation, restaurant lookup) should change independently

This is *exactly* why the three patterns show up:

| Problem | Pattern | Why it fits |
| --- | --- | --- |
| Need exactly one global registry of restaurants / orders | **Singleton** | One shared source of truth, globally accessible |
| Need to create different *kinds* of orders without the client caring how | **Factory Method** | Decouples "what order to build" from "who's asking for it" |
| Need to swap payment methods without touching `Order` | **Strategy** | Payment algorithm becomes interchangeable at runtime |

---

## 2. High-Level Flow

```
User → search restaurants (by location) → RestaurantManager
     → pick Restaurant → browse MenuItems
     → add MenuItems to Cart
     → checkout → IOrderFactory creates an Order (Delivery/Pickup)
     → Order.strategy.pay() → IPaymentStrategy
     → OrderManager stores the Order
     → NotificationService.notifyUser()
```

`Tomato` sits above all of this as the **orchestration class** — it doesn't hold long-term state itself, it *coordinates* calls between `User`, `RestaurantManager`, `Cart`, `IOrderFactory`, `OrderManager`, and `NotificationService`. (This role is basically a **Facade**, even though you haven't formally covered that pattern yet — worth knowing the name for later.)

---

## 3. Class Catalog

### `Restaurant` «Model»

```
int restaurantId
String name
String loc
Vector<MenuItem> menu
```

Plain data holder representing a restaurant.

### `MenuItem` «Model»

```
- code: String
- name: String
- price: int
// getters & setters
```

Plain data holder for one dish.

### `RestaurantManager` «Singleton»

```
Vector<Restaurant> restaurants
addRestaurant(Restaurant r)
searchByLoc(loc)
```

One global registry of all restaurants on the platform. Singleton because there's only ever *one* master list — you don't want five different managers each with a different partial view of restaurants.

### `User` «Model»

```
int userid
String name
String address
Cart cart
```

Each logged-in user, with their own personal shopping cart.

### `Cart`

```
Restaurant* r
Vector<MenuItem> items
addToCart(MenuItem it)
totalCost()
isEmpty()
```

Temporary, per-user shopping session. Holds a reference to *which* restaurant the user is ordering from, plus the items picked so far.

### `IOrderFactory` «Interface»

```
createOrder()
```

Abstract creator — declares *that* an order gets created without saying *how*.

### `NowOrderFactory` / `ScheduleOrderFactory`

```
createOrder(type) {}
// ScheduleOrderFactory also has: String scheduleTime
```

Concrete factories. `NowOrderFactory` builds an order for immediate fulfillment; `ScheduleOrderFactory` builds one for a future time slot.

### `Order` (abstract)

```
int id
User user
Restaurant* rest
Vector<MenuItem> items
PaymentStrategy strategy
getType()
```

Base order record. Abstract because "an order" is never *just* an order — it's always either delivery or pickup.

### `DeliveryOrder` / `PickupOrder`

```
DeliveryOrder: String address;      getType(){}
PickupOrder:   String resAddress;   getType(){}
```

Concrete order types, each overriding `getType()` and carrying type-specific data (drop-off address vs. pickup location).

### `OrderManager` «Singleton»

```
Vector<Order> orderList
addOrder(order)
listOrder()
```

One global ledger of every order ever placed — same reasoning as `RestaurantManager`.

### `IPaymentStrategy` «Interface»

```
pay()
```

### `CreditCard` / `NetBanking` / `UPI`

```
pay() {}
```

Interchangeable payment algorithms — `Order` doesn't know or care which one it's holding.

### `NotificationService`

```
Order order
notifyUser()
```

Fires a notification once given an order.

### `Tomato`

Orchestration / client-facing entry point. No persistent attributes of its own — it *uses* the other classes.

---

## 4. Relationships — What, Between Whom, and *Why*

This is the part you specifically asked about. Quick vocabulary refresher first:

| Term | Meaning | Lifecycle |
| --- | --- | --- |
| **Association** | "uses-a" / "knows about" — one class references another | Both live independently |
| **Aggregation** (hollow ◇) | "has-a", weak whole-part | Part can outlive the whole |
| **Composition** (filled ◆) | "has-a", strong whole-part | Part dies when the whole dies |
| **Inheritance** (`▷` hollow triangle, solid line) | "is-a" | Subclass *is* a specialized version of parent |
| **Realization** (`▷` hollow triangle, dashed line) | "implements" | Class fulfills an interface's contract, no shared code |
| **Dependency** (dashed arrow) | "temporarily uses" | One class calls/creates another but doesn't store it long-term |

Now, mapped onto your diagram:

### Composition (filled diamond — part cannot exist without the whole)

| Relationship | Multiplicity | Why it's composition, not aggregation |
| --- | --- | --- |
| `Restaurant` ◆— `MenuItem` | 1 restaurant → many MenuItems | A menu item is meaningless without its parent restaurant. If the restaurant is deleted, its menu items should be deleted too — they don't belong to anything else. |
| `User` ◆— `Cart` | 1 user → 1 cart | A cart has no independent identity outside its owner. It's created with the user's session and destroyed with it — never shared or reassigned to another user. |

### Aggregation (hollow diamond — whole "has" parts, but parts survive independently)

| Relationship | Multiplicity | Why it's aggregation, not composition |
| --- | --- | --- |
| `RestaurantManager` ◇— `Restaurant` | 1 manager → many restaurants | Restaurants exist as real-world businesses independent of whether *this particular manager object* is holding a reference to them. The manager is just an organizing registry. |
| `OrderManager` ◇— `Order` | 1 manager → many orders | Same logic — `OrderManager` is a log/registry. Conceptually the order record's "meaning" doesn't depend on the manager object existing; the manager just tracks it. |
| `Cart` ◇— `MenuItem` | 1 cart → many items | The `MenuItem` already belongs to the restaurant's menu (that's the composition above). The cart just *references* items temporarily — clearing the cart doesn't delete the dish from the menu. |

> ⚠️ **Note on your diagram:** your sketch draws the same crosshatched diamond symbol everywhere (Restaurant–MenuItem, RestaurantManager–Restaurant, Cart–MenuItem, OrderManager–Order). In strict UML these should look different — **filled diamond = composition**, **hollow/empty diamond = aggregation**. Worth fixing visually next time so the diagram self-documents the lifecycle rule, not just the "has multiple" fact.

### Plain Association (reference only, no ownership implied either way)

| Relationship | Why |
| --- | --- |
| `Cart` → `Restaurant` (`Restaurant* r`) | Cart just needs to *know which* restaurant it's ordering from. It doesn't own the restaurant's lifecycle in either direction. |
| `Order` → `User`, `Order` → `Restaurant`, `Order` → `IPaymentStrategy` | Order references an already-existing user, restaurant, and chosen payment strategy — none of these are created *for* or destroyed *by* the order. |
| `NotificationService` → `Order` | It just needs an order reference at the moment of notifying — no ownership. |

### Inheritance / "is-a"

| Relationship | Why it's is-a, not has-a |
| --- | --- |
| `DeliveryOrder` ▷ `Order` | A delivery order *is* an order, just with delivery-specific behavior (`getType()` returns "delivery", carries a drop address). |
| `PickupOrder` ▷ `Order` | Same reasoning — it's a specialization, not a component. |

### Realization / "implements"

| Relationship | Why |
| --- | --- |
| `NowOrderFactory`, `ScheduleOrderFactory` ⇢ `IOrderFactory` | Both fulfill the contract "you must be able to `createOrder()`" but share no inherited code — that's realization, not inheritance. |
| `CreditCard`, `NetBanking`, `UPI` ⇢ `IPaymentStrategy` | Each independently implements `pay()` its own way — classic Strategy pattern realization. |

### Dependency (uses temporarily, doesn't store)

| Relationship | Why |
| --- | --- |
| `IOrderFactory` ⇢ `Order` | The factory *creates* an `Order`/`DeliveryOrder`/`PickupOrder` and hands it back — it doesn't keep holding onto it afterward. |
| `Tomato` ⇢ (`RestaurantManager`, `Cart`, `IOrderFactory`, `OrderManager`, `NotificationService`) | Tomato calls into these to orchestrate a request; it's not a permanent attribute-holding relationship, it's "uses during this operation." |

---

## 5. Is-a vs Has-a — Quick Gut Check

A trick for future diagrams: ask **"can I truthfully finish the sentence '*X is a Y*'?"**

- "A DeliveryOrder is an Order" ✅ → inheritance
- "A MenuItem is a Restaurant" ❌ → so it must be has-a (composition, since it can't survive without the restaurant)
- "A CreditCard is a PaymentStrategy" — sort of, but really it's "*implements the ability to* pay" → realization (interface, no shared state/code)
- "A Cart is a Restaurant" ❌, and "the restaurant doesn't need the cart to exist" → plain association, not even aggregation

---

## 6. Things Worth Double-Checking / Rethinking

1. **`createOrder(type)` parameter overload:** Your `NowOrderFactory`/`ScheduleOrderFactory` both take a `type` param, but it's ambiguous whether `type` means *Delivery vs Pickup* or something else — because *when* (now/scheduled) and *how* (delivery/pickup) are two independent dimensions. Right now the diagram conflates them into one factory hierarchy. Two clean options:
   - Keep one `IOrderFactory` hierarchy, and have `createOrder(type)` take an enum `{DELIVERY, PICKUP}` to decide the concrete `Order` subclass, while the *Now vs Schedule* factory decides scheduling metadata before construction.
   - Or split into two independent factory hierarchies if "how" and "when" can vary independently in your real system (e.g., a scheduled pickup order should be valid too).
2. **`OrderManager` vs `Order` — aggregation vs composition:** I called it aggregation above (an order "makes sense" without the manager), but you could argue for composition if, in your system, an `Order` is *never* meant to exist outside the manager's list (i.e., it's created solely to be tracked). Either is defensible — just be intentional and consistent about which one you pick, and note it as a design decision.
3. **`Restaurant* r` and `Restaurant* rest` (raw pointers):** fine for a UML sketch / C++-flavored pseudocode, but if you implement this in Java/Python/JS, these just become plain object references — no behavior change to the relationship, just a note that "has-a via pointer" and "has-a via reference" mean the same thing here.

---

## 7. Design Pattern Cheat-Sheet (mapped to this project)

| Pattern | Interface/Abstract | Concrete Implementations | Who uses it |
| --- | --- | --- | --- |
| Singleton | — | `RestaurantManager`, `OrderManager` | Anyone needing the one global list |
| Factory Method | `IOrderFactory` | `NowOrderFactory`, `ScheduleOrderFactory` | `Tomato` when checkout is triggered |
| Strategy | `IPaymentStrategy` | `CreditCard`, `NetBanking`, `UPI` | `Order` at payment time |