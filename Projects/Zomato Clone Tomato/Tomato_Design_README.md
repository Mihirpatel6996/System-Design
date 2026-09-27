# Tomato — Food Delivery System

A learning-oriented object-oriented design for a small food-delivery application inspired by apps such as Zomato.

This document converts the UML diagram and rough notes into a readable, dependency-first design.

The important goal is **not only to know what each class does**, but to understand **why each UML relationship exists**:

- Association
- Aggregation
- Composition
- Generalization / Inheritance (`is-a`)
- Realization / Interface implementation
- Dependency
- `has-a` as a general object-oriented relationship

The classes are intentionally explained from the **bottom level upward**. A class is introduced only after the classes it depends on have already been explained.

---

# 1. Functional Requirements

The system should support the following operations:

1. A user can search for restaurants based on location.
2. A user can select a restaurant and add menu items to a cart.
3. A user can check out and place an order.
4. The user can choose a payment method.
5. The system supports multiple payment strategies:
   - Credit Card
   - Net Banking
   - UPI
   - Other future payment methods
6. The system supports multiple order types:
   - Delivery Order
   - Pickup Order
7. The system can create different order types without exposing object-creation logic to the client.
8. The system stores/manages orders.
9. The user is notified after an order is successfully placed.
10. The major parts of the design should be scalable and modifiable.

---

# 2. Non-Functional Requirements

The rough requirement says:

> Each part of the design should be scalable and modifiable.

In design terms, this means we want:

- Low coupling where possible.
- High cohesion inside each class.
- New payment methods should not require large changes to `Order`.
- New order types should not require large changes to the client.
- Restaurant management should be independent from order management.
- Object creation should be separated from business logic.
- Notification logic should be replaceable.
- Shared managers should have controlled access.

The design patterns being practiced here are:

| Pattern | Where it is used |
|---|---|
| Singleton | `RestaurantManager`, `OrderManager` |
| Strategy | `IPaymentStrategy` + payment implementations |
| Factory | `IOrderFactory` + `NewOrderFactory` + `ScheduledOrderFactory` |

---

# 3. Dependency-First Architecture

The system is intentionally learned in this order:

```text
MenuItem
   ↓
Restaurant
   ↓
RestaurantManager
   ↓
User
   ↓
Cart
   ↓
IPaymentStrategy
   ↓
Payment Implementations
   ↓
Order
   ↓
DeliveryOrder / PickupOrder
   ↓
IOrderFactory
   ↓
NewOrderFactory / ScheduledOrderFactory
   ↓
OrderManager
   ↓
NotificationService
   ↓
Tomato
```

There is one important clarification:

`User` does not necessarily have a direct UML relationship with every restaurant.

A user can **interact with restaurants through the restaurant-management/search functionality**, while the `Cart` contains the currently selected restaurant and menu items.

---

# 4. UML Relationship Vocabulary

Before reading the classes, understand these terms.

## 4.1 Association

Association means:

> One object knows about, uses, or is connected to another object.

Example:

```text
Cart ---- Restaurant
```

A cart refers to a restaurant, but the restaurant does not depend on the cart for its existence.

This is the most general relationship.

---

## 4.2 Has-a

`has-a` is an informal object-oriented description.

For example:

```text
Cart has-a Restaurant
Order has-a PaymentStrategy
User has-a Cart
```

However:

> Not every `has-a` relationship is composition.

Composition and aggregation are **stronger forms of ownership**.

---

## 4.3 Aggregation

Aggregation means:

> One object groups/manages other objects, but the contained objects can exist independently.

Example:

```text
RestaurantManager ◇---- Restaurant
```

The manager keeps a collection of restaurants.

If the manager disappears, the restaurants still conceptually exist.

Therefore:

```text
RestaurantManager has-many Restaurants
```

is a good aggregation example.

---

## 4.4 Composition

Composition means:

> The contained object strongly belongs to the owner, and its lifecycle is tied to the owner.

Example:

```text
User ◆---- Cart
```

In this model, the cart is treated as belonging to the user.

If that user object is removed, its owned cart is also considered part of that lifecycle.

Another example:

```text
Restaurant ◆---- MenuItem
```

The design assumes the menu items are owned by the restaurant.

A menu item in this model is not an independent menu entity floating around without a restaurant.

---

## 4.5 Generalization / Inheritance

This represents:

```text
is-a
```

Example:

```text
DeliveryOrder is-a Order
PickupOrder   is-a Order
```

The child class inherits common behavior and data from the parent.

---

## 4.6 Realization

Realization means:

> A concrete class implements an interface.

Example:

```text
CreditCard ----|> IPaymentStrategy
```

Conceptually:

```text
CreditCard is-a PaymentStrategy
```

More precisely:

```text
CreditCard implements IPaymentStrategy
```

---

## 4.7 Dependency

Dependency means:

> One class temporarily uses another class to perform some operation.

For example:

```text
NewOrderFactory --> DeliveryOrder
```

The factory depends on `DeliveryOrder` because it creates it.

A dependency is weaker than composition.

---

# 5. Class 1 — MenuItem

## Purpose

`MenuItem` represents a food item offered by a restaurant.

Examples:

```text
Pizza
Burger
Biryani
Coffee
```

## Structure

```java
class MenuItem {
    String code;
    String name;
    int price;

    getters();
}
```

## Data

```text
code
name
price
```

## Why does MenuItem come first?

Almost every higher-level object eventually needs menu items.

A restaurant contains menu items.

A cart contains selected menu items.

An order records menu items.

Therefore, `MenuItem` is one of the lowest-level domain objects in this model.

## Relationships

At this level, `MenuItem` does not depend on any other domain class.

That is why it is introduced first.

---

# 6. Class 2 — Restaurant

## Purpose

`Restaurant` represents a restaurant available on the platform.

## Structure

```java
class Restaurant {
    int restaurantId;
    String name;
    String address;

    vector<MenuItem> menu;
}
```

## Relationship

```text
Restaurant ◆---- MenuItem
        1        0..*
```

This is **composition** in the current model.

### Why composition?

The design says:

> Menu items belong to a restaurant.

The restaurant owns its menu.

Conceptually:

```text
Restaurant
    |
    +-- MenuItem
    +-- MenuItem
    +-- MenuItem
```

If the restaurant is removed from this model, its owned menu entries are also removed.

Therefore:

```text
Restaurant has-a MenuItem
```

with strong lifecycle ownership:

```text
Restaurant composes MenuItems
```

## Multiplicity

```text
One Restaurant -> zero or many MenuItems
```

```text
1 ---- 0..*
```

A restaurant may temporarily have no menu items, and usually has many.

---

# 7. Class 3 — RestaurantManager

## Purpose

`RestaurantManager` manages the collection of restaurants.

Typical responsibilities:

```text
addRestaurant()
removeRestaurant()
updateRestaurant()
searchByLocation()
```

The rough design also includes:

```java
vector<Restaurant> restaurants;
```

## Singleton

The UML marks this class as:

```text
<<Singleton>>
```

The intention is to have one shared restaurant-management object in the application.

The Singleton pattern is about **instance control**.

It is not itself a UML association such as aggregation or composition.

Those are separate ideas.

---

## Relationship with Restaurant

```text
RestaurantManager ◇---- Restaurant
                  1     0..*
```

This is **aggregation**.

### Why aggregation?

The manager stores/manages restaurants:

```java
vector<Restaurant> restaurants;
```

But the manager is not the owner of the restaurant's entire lifecycle.

For example:

```text
Restaurant exists
        |
        v
RestaurantManager manages it
```

If the manager object is destroyed, the restaurant concept should still exist independently.

Therefore:

```text
RestaurantManager has-many Restaurants
```

but:

```text
RestaurantManager does not own the lifecycle of Restaurant
```

That is why aggregation is more appropriate than composition.

---

## Dependency

`RestaurantManager` depends on `Restaurant` because it:

- stores `Restaurant` objects,
- adds restaurants,
- searches restaurants,
- performs CRUD operations on them.

---

# 8. Class 4 — User

## Purpose

`User` represents the customer using the system.

## Structure

```java
class User {
    int userId;
    String name;
    String address;

    Cart cart;
}
```

The diagram shows:

```text
Cart cart;
```

---

# 9. User -> Cart

```text
User ◆---- Cart
       1    1
```

This is modeled as **composition**.

## Why?

The current design treats the cart as belonging to the user.

Conceptually:

```text
User
 |
 +---- Cart
```

The cart is the user's current shopping state.

If the user object goes away, the user's owned cart goes away as well.

Therefore:

```text
User has-a Cart
```

and, under this model:

```text
User composes Cart
```

### Important distinction

`has-a` is the general relationship.

`composition` adds a stronger ownership/lifecycle meaning.

So:

```text
User has-a Cart
```

is true.

And the UML design further specifies:

```text
User compositionally owns that Cart
```

---

# 10. Class 5 — Cart

## Purpose

`Cart` represents the user's current shopping cart.

## Structure

```java
class Cart {
    Restaurant restaurant;
    vector<MenuItem> items;

    void addToCart(MenuItem item);
    void clear();
    int total();
    bool isEmpty();
}
```

The cart belongs to a user and is associated with the selected restaurant and menu items.

---

# 11. Cart -> Restaurant

```text
Cart ---- Restaurant
```

This is best modeled as a **plain association**.

## Why not composition?

The restaurant already exists independently.

The cart does not create or destroy the restaurant.

The relationship means:

```text
Cart knows which Restaurant these items belong to.
```

So:

```text
Cart has-a Restaurant
```

but not:

```text
Cart composes Restaurant
```

---

# 12. Cart -> MenuItem

```text
Cart ---- MenuItem
```

This is also a **plain association** in the current model.

## Why?

The cart refers to menu items selected by the customer.

But the menu item is still owned by the restaurant.

The cart should not be responsible for creating or destroying the restaurant's menu item.

Therefore:

```text
Cart has selected MenuItems
```

but:

```text
Cart does not own the MenuItems
```

So composition would be too strong here.

---

## Important real-world improvement

The current model has:

```text
vector<MenuItem> items
```

A production food-delivery design would usually introduce:

```text
CartItem
    MenuItem item
    int quantity
```

because a customer can buy:

```text
Burger x 2
Pizza x 1
```

Similarly, an order usually needs an `OrderItem` to preserve:

- quantity,
- price at purchase time,
- item name at purchase time.

This is a useful future improvement, but the current diagram can remain as-is while learning the patterns.

---

# 13. Payment Strategy

Payment is the first major Strategy Pattern area.

The requirement is:

```text
The user can pay using different payment methods.
```

Potential methods:

```text
Credit Card
Net Banking
UPI
...
```

A naive implementation might put:

```java
if (paymentType == CREDIT_CARD) ...
else if (paymentType == UPI) ...
else if (paymentType == NET_BANKING) ...
```

inside `Order`.

That would make `Order` grow every time a new payment method is introduced.

Instead, use the Strategy Pattern.

---

# 14. Class — IPaymentStrategy

```java
interface IPaymentStrategy {
    void pay();
}
```

This is the abstraction for payment behavior.

The important idea is:

```text
Order does not need to know HOW payment is performed.
Order only knows that it has a payment strategy.
```

---

# 15. Payment Implementations

## CreditCard

```java
class CreditCard implements IPaymentStrategy {
    void pay() {
        ...
    }
}
```

## NetBanking

```java
class NetBanking implements IPaymentStrategy {
    void pay() {
        ...
    }
}
```

## UPI

```java
class UPI implements IPaymentStrategy {
    void pay() {
        ...
    }
}
```

---

# 16. Payment Relationships

```text
             IPaymentStrategy
              /      |      \
             /       |       \
     CreditCard   NetBanking   UPI
```

These are **realization / implementation** relationships.

Conceptually:

```text
CreditCard implements IPaymentStrategy
NetBanking implements IPaymentStrategy
UPI implements IPaymentStrategy
```

This can also be thought of as:

```text
CreditCard is-a PaymentStrategy
NetBanking is-a PaymentStrategy
UPI is-a PaymentStrategy
```

The interface defines the contract:

```text
pay()
```

Each concrete class decides how that payment is performed.

---

# 17. Why Strategy Works Here

The part that changes is:

```text
PAYMENT METHOD
```

The overall order-processing logic does not need to change.

For example:

```java
Order order;
order.setPaymentStrategy(new UPI());
order.pay();
```

Then later:

```java
order.setPaymentStrategy(new CreditCard());
order.pay();
```

The `Order` class delegates payment behavior to the selected strategy.

This is the core idea of Strategy:

> Encapsulate interchangeable behavior behind an abstraction.

---

# 18. Class 6 — Order

`Order` is the central business object created after checkout.

## Structure

```java
class Order {
    int id;

    User user;
    Restaurant restaurant;
    vector<MenuItem> items;

    IPaymentStrategy paymentStrategy;

    OrderType getType();
}
```

---

# 19. Order Relationships

## Order -> User

```text
Order ---- User
```

### Type

Association.

### Why?

An order records who placed it.

The order does not own the user's lifecycle.

```text
Order knows User
```

but:

```text
Order does not create/destroy User
```

---

## Order -> Restaurant

```text
Order ---- Restaurant
```

### Type

Association.

### Why?

The order records where the food came from.

The restaurant exists independently of the order.

---

## Order -> MenuItem

```text
Order ---- MenuItem
```

### Type in the current diagram

Association.

The order records which items were ordered.

The restaurant owns the menu items; the order should not own the restaurant's menu lifecycle.

### Important production note

A real system should usually create:

```text
Order
  |
  +-- OrderItem
       |
       +-- MenuItem reference
       +-- quantity
       +-- purchased price
       +-- purchased name
```

Then `Order` could **compose `OrderItem`** because the order owns the order-line records.

That solves an important real-world problem:

```text
Restaurant changes Pizza price from 200 -> 250

Old Order must still show:

Pizza = 200
```

Therefore an order should normally store a purchase-time snapshot instead of depending on a mutable current menu price.

---

## Order -> IPaymentStrategy

```text
Order ---- IPaymentStrategy
```

### Type

Association / `has-a`.

The Strategy Pattern is being used through **object composition/delegation**.

The order contains or receives a payment strategy:

```text
Order
 |
 +---- IPaymentStrategy
```

The important distinction is:

```text
has-a strategy
```

does not automatically mean UML **composition**.

Composition is specifically about lifecycle ownership.

The strategy is better modeled as an association unless the design explicitly guarantees lifecycle ownership.

---

# 20. Why Order Comes After PaymentStrategy

`Order` contains:

```text
IPaymentStrategy paymentStrategy;
```

Therefore, when learning the system from the bottom upward, the payment abstraction should already be understood.

This is why the dependency-first sequence is:

```text
Cart
   ↓
IPaymentStrategy
   ↓
Payment implementations
   ↓
Order
```

---

# 21. Order Type — DeliveryOrder and PickupOrder

There are two kinds of orders.

```text
DeliveryOrder
PickupOrder
```

Both share common order behavior.

Therefore we create a parent class:

```text
Order
```

and derive the two specialized types.

---

# 22. DeliveryOrder

```java
class DeliveryOrder : public Order {
    String address;

    OrderType getType() {
        return DELIVERY;
    }
}
```

---

# 23. PickupOrder

```java
class PickupOrder : public Order {
    String pickupLocation;

    OrderType getType() {
        return PICKUP;
    }
}
```

---

# 24. Order -> DeliveryOrder / PickupOrder

```text
                Order
               /     \
              /       \
     DeliveryOrder   PickupOrder
```

This is **generalization / inheritance**.

It represents:

```text
DeliveryOrder is-a Order
PickupOrder is-a Order
```

The subclasses inherit the common properties:

```text
id
user
restaurant
items
paymentStrategy
```

and add their own specialized information.

---

# 25. Why Inheritance Here?

Suppose both order types contain:

```text
id
user
restaurant
items
paymentStrategy
```

Putting all of that into both classes would duplicate code.

Instead:

```text
Order
 |
 +-- common state/behavior
 |
 +-- DeliveryOrder
 |
 +-- PickupOrder
```

The parent holds what is common.

The children hold what is specialized.

---

# 26. Class — IOrderFactory

Now we have several concrete order types.

Something must decide:

```text
Which Order object should be created?
```

That responsibility belongs to a factory.

First define the factory interface.

```java
interface IOrderFactory {
    Order createOrder(...);
}
```

The important point is that the factory returns the abstraction:

```text
Order
```

rather than forcing the client to directly construct concrete subclasses.

---

# 27. NewOrderFactory

```java
class NewOrderFactory implements IOrderFactory {
    Order createOrder(...) {
        ...
    }
}
```

Its responsibility is object creation for a normal/new order flow.

---

# 28. ScheduledOrderFactory

```java
class ScheduledOrderFactory implements IOrderFactory {
    String scheduledTime;

    Order createOrder(...) {
        ...
    }
}
```

This factory handles the scheduled-order flow.

---

# 29. Factory Relationships

```text
                IOrderFactory
                 /        \
                /          \
   NewOrderFactory     ScheduledOrderFactory
```

The concrete factories **realize/implement** the interface.

Therefore:

```text
NewOrderFactory implements IOrderFactory
ScheduledOrderFactory implements IOrderFactory
```

---

# 30. Factory Dependency on Order Types

The factories create concrete orders.

Therefore a factory has a **dependency** on the order classes it constructs.

Conceptually:

```text
NewOrderFactory --------> Order / concrete Order type
ScheduledOrderFactory --> Order / concrete Order type
```

This is a creation dependency.

The factory needs the class to create an object.

---

# 31. Why Factory Pattern?

Without a factory, client code may become:

```java
if (type == DELIVERY) {
    order = new DeliveryOrder(...);
}
else if (type == PICKUP) {
    order = new PickupOrder(...);
}
```

Every caller would need to know concrete classes.

With a factory:

```java
Order order = factory.createOrder(...);
```

The caller asks for an order without directly managing construction details.

This reduces the amount of creation logic spread across the application.

---

# 32. Class — OrderManager

## Purpose

`OrderManager` manages created orders.

## Structure

```java
class OrderManager {
    vector<Order> orderList;

    void addOrder(Order order);
    ...
}
```

The UML marks it as:

```text
<<Singleton>>
```

---

# 33. OrderManager -> Order

```text
OrderManager ◇---- Order
               1    0..*
```

This is **aggregation**.

## Why?

`OrderManager` maintains a collection:

```java
vector<Order> orderList;
```

but the orders do not fundamentally exist because of the manager.

An order is created elsewhere and then registered with the manager.

So:

```text
Order exists independently
        |
        v
OrderManager manages it
```

That is aggregation.

---

# 34. OrderManager Singleton vs Aggregation

These are two different design decisions.

### Singleton answers:

```text
How many OrderManager instances should exist?
```

Answer:

```text
One shared instance.
```

### Aggregation answers:

```text
What relationship does OrderManager have with Order?
```

Answer:

```text
It manages/collects Orders that can exist independently.
```

Do not mix these concepts.

---

# 35. Class — NotificationService

## Purpose

`NotificationService` informs the user that an order was successfully placed.

Example:

```java
class NotificationService {
    Order order;

    void notifyUser();
}
```

---

# 36. NotificationService -> Order

If `NotificationService` stores an `Order` member:

```java
Order order;
```

then the relationship can be represented as an **association**.

```text
NotificationService ---- Order
```

The service knows which order it is notifying about.

If instead the method were:

```java
void notifyUser(Order order);
```

and the service did not keep the order as state, the relationship would be better represented as a **dependency**.

This is an important UML lesson:

> The exact class design matters when deciding between association and dependency.

---

# 37. Class — Tomato

`Tomato` is the application-level class that interacts with the client.

Think of it as an application entry point / orchestrator.

Its responsibility is not to own every business object.

Instead, it coordinates the workflow.

Possible responsibilities include:

```text
search restaurants
select restaurant
manage cart
choose payment strategy
create order
store order
trigger notification
```

---

# 38. Tomato Relationships

`Tomato` interacts with many parts of the system.

Conceptually:

```text
Client
  |
  v
Tomato
  |
  +--> RestaurantManager
  |
  +--> User
  |
  +--> Cart
  |
  +--> OrderFactory
  |
  +--> OrderManager
  |
  +--> NotificationService
```

These are generally **dependencies** or application-level associations depending on whether `Tomato` merely uses an object temporarily or stores it as state.

For an orchestrator, dependency is usually the safer interpretation.

---

# 39. Complete Dependency-First Structure

Now that every class has been explained:

```text
1. MenuItem
      |
      v
2. Restaurant
      |
      v
3. RestaurantManager
      |
      v
4. User
      |
      v
5. Cart
      |
      v
6. IPaymentStrategy
      |
      +---- CreditCard
      +---- NetBanking
      +---- UPI
      |
      v
7. Order
      |
      +---- DeliveryOrder
      |
      +---- PickupOrder
      |
      v
8. IOrderFactory
      |
      +---- NewOrderFactory
      +---- ScheduledOrderFactory
      |
      v
9. OrderManager
      |
      v
10. NotificationService
      |
      v
11. Tomato
```

---

# 40. Relationship Summary Table

| From | To | Relationship | Why |
|---|---|---|---|
| `Restaurant` | `MenuItem` | Composition | Restaurant owns the menu items in this model |
| `RestaurantManager` | `Restaurant` | Aggregation | Manager stores/manages restaurants, but restaurants exist independently |
| `User` | `Cart` | Composition | Cart is modeled as the user's owned shopping state |
| `Cart` | `Restaurant` | Association | Cart refers to selected restaurant; it does not own it |
| `Cart` | `MenuItem` | Association | Cart selects menu items; restaurant owns them |
| `CreditCard` | `IPaymentStrategy` | Realization | CreditCard implements the payment interface |
| `NetBanking` | `IPaymentStrategy` | Realization | NetBanking implements the payment interface |
| `UPI` | `IPaymentStrategy` | Realization | UPI implements the payment interface |
| `Order` | `User` | Association | Order records who placed it |
| `Order` | `Restaurant` | Association | Order records the restaurant |
| `Order` | `MenuItem` | Association | Order records ordered items in the current model |
| `Order` | `IPaymentStrategy` | Association / has-a | Order delegates payment behavior to a strategy |
| `DeliveryOrder` | `Order` | Inheritance | DeliveryOrder is-a Order |
| `PickupOrder` | `Order` | Inheritance | PickupOrder is-a Order |
| `NewOrderFactory` | `IOrderFactory` | Realization | Implements factory contract |
| `ScheduledOrderFactory` | `IOrderFactory` | Realization | Implements factory contract |
| `NewOrderFactory` | `Order` / concrete order type | Dependency | Factory creates orders |
| `ScheduledOrderFactory` | `Order` / concrete order type | Dependency | Factory creates orders |
| `OrderManager` | `Order` | Aggregation | Manager stores/manages independent orders |
| `NotificationService` | `Order` | Association or Dependency | Depends on whether it stores the order or only receives it as an argument |
| `Tomato` | application services/classes | Dependency | Application layer orchestrates the system |

---

# 41. Complete "Has-a" View

A useful way to mentally visualize the system is:

```text
Restaurant
    has-a collection of MenuItems

RestaurantManager
    has-a collection of Restaurants

User
    has-a Cart

Cart
    has-a Restaurant
    has-a collection of selected MenuItems

Order
    has-a User
    has-a Restaurant
    has-a collection of MenuItems
    has-a PaymentStrategy

OrderManager
    has-a collection of Orders

NotificationService
    knows/uses an Order

Tomato
    uses the application components
```

But remember:

```text
has-a != automatically composition
```

The exact ownership/lifecycle determines whether the relationship is:

```text
association
aggregation
composition
```

---

# 42. Complete "Is-a" View

The `is-a` relationships are:

```text
DeliveryOrder is-a Order
PickupOrder is-a Order
```

and, through interface realization:

```text
CreditCard is-a IPaymentStrategy
NetBanking is-a IPaymentStrategy
UPI is-a IPaymentStrategy
```

Factory implementations:

```text
NewOrderFactory is-a IOrderFactory
ScheduledOrderFactory is-a IOrderFactory
```

More precisely, the latter two are:

```text
implements IOrderFactory
```

---

# 43. Complete Composition View

The important composition relationships in the current design are:

```text
Restaurant ◆---- MenuItem
User       ◆---- Cart
```

Meaning:

```text
Restaurant owns MenuItems
User owns Cart
```

A future improved model could also introduce:

```text
Order ◆---- OrderItem
Cart  ◆---- CartItem
```

because cart lines and order lines belong to their corresponding cart/order.

---

# 44. Complete Aggregation View

The aggregation relationships are:

```text
RestaurantManager ◇---- Restaurant
OrderManager      ◇---- Order
```

Meaning:

```text
RestaurantManager manages Restaurants
OrderManager manages Orders
```

The managed objects can exist independently.

---

# 45. Payment Flow

```text
User
 |
 | selects payment method
 v
IPaymentStrategy
 |
 +---- UPI
 +---- CreditCard
 +---- NetBanking
```

Then:

```text
Order
 |
 +---- paymentStrategy.pay()
```

The order does not need to know the internal implementation of:

```text
UPI
CreditCard
NetBanking
```

This is the Strategy Pattern.

---

# 46. Order Creation Flow

```text
Client
  |
  v
Tomato
  |
  v
IOrderFactory
  |
  +---- NewOrderFactory
  |         |
  |         v
  |      Order
  |
  +---- ScheduledOrderFactory
            |
            v
          Order
```

Factory logic decides which object should be created.

---

# 47. Complete Business Flow

The business flow can be expressed as:

```text
User
  |
  | search by location
  v
RestaurantManager
  |
  v
Restaurants
  |
  | select restaurant
  v
Cart
  |
  | add MenuItems
  v
Checkout
  |
  | select PaymentStrategy
  v
OrderFactory
  |
  | create order
  v
DeliveryOrder / PickupOrder
  |
  | add to manager
  v
OrderManager
  |
  | notify
  v
NotificationService
  |
  v
User
```

---

# 48. Why Dependency-First Learning Works

The dependency-first order is useful because each class builds on concepts already known.

For example:

```text
MenuItem
```

does not need anything else.

Then:

```text
Restaurant
```

needs `MenuItem`.

Then:

```text
RestaurantManager
```

needs `Restaurant`.

Then:

```text
Cart
```

needs restaurant/menu-item concepts.

Then:

```text
Order
```

needs user, restaurant, menu items, and payment strategy.

Then:

```text
Factory
```

needs order types.

Then:

```text
OrderManager
```

needs orders.

Then:

```text
NotificationService
```

needs order information.

Finally:

```text
Tomato
```

coordinates the already-understood components.

This prevents the common problem of encountering a class that refers to five other classes that have not yet been explained.

---

# 49. Pattern Map

## Singleton

```text
RestaurantManager
OrderManager
```

Purpose:

```text
Restrict/coordinate creation of a shared manager instance.
```

---

## Strategy

```text
IPaymentStrategy
      |
      +---- CreditCard
      +---- NetBanking
      +---- UPI
```

Purpose:

```text
Encapsulate interchangeable payment behavior.
```

---

## Factory

```text
IOrderFactory
      |
      +---- NewOrderFactory
      +---- ScheduledOrderFactory
```

Purpose:

```text
Encapsulate order object creation.
```

---

# 50. A Very Important Design Distinction

Do not memorize relationship names mechanically.

Instead ask these questions.

## Question 1 — Does it simply know/use another object?

```text
Association
```

Example:

```text
Cart ---- Restaurant
```

---

## Question 2 — Does it group/manage objects that can live independently?

```text
Aggregation
```

Example:

```text
OrderManager ◇---- Order
```

---

## Question 3 — Does it strongly own the object's lifecycle?

```text
Composition
```

Example:

```text
Restaurant ◆---- MenuItem
```

---

## Question 4 — Is it a specialized form of another class?

```text
Inheritance / is-a
```

Example:

```text
DeliveryOrder is-a Order
```

---

## Question 5 — Does it implement an interface?

```text
Realization
```

Example:

```text
UPI implements IPaymentStrategy
```

---

## Question 6 — Does it only use another class for some operation?

```text
Dependency
```

Example:

```text
Factory --> ConcreteOrder
```

because the factory uses that class to create an object.

---

# 51. One Important Correction to the Rough Notes

The statement:

```text
User -> multiple restaurants
```

should not automatically become a direct association in the class diagram.

There are two different concepts:

### Business interaction

A user can:

```text
search many restaurants
visit many restaurants
place orders from restaurants
```

### Object ownership/reference

That does not mean:

```text
User has-a vector<Restaurant>
```

unless the implementation actually needs to store that relationship.

This is a very important UML lesson:

> A real-world interaction does not automatically need to become a class member or a UML association.

Only model a structural relationship when the software design actually needs that relationship.

---

# 52. Current Architecture at a Glance

```text
                         +----------------+
                         |     Tomato     |
                         +----------------+
                          /      |       \
                         /       |        \
                        v        v         v
             RestaurantManager   OrderFactory   NotificationService
                    |                |                  |
                    v                v                  v
               Restaurant          Order                 Order
                    |
                    v
                MenuItem

User
 |
 | composition
 v
Cart
 |
 +---- Restaurant
 |
 +---- MenuItems

Order
 |
 +---- User
 +---- Restaurant
 +---- MenuItems
 +---- IPaymentStrategy
             |
             +---- CreditCard
             +---- NetBanking
             +---- UPI

Order
 |
 +---- DeliveryOrder
 |
 +---- PickupOrder

OrderManager
 |
 +---- Orders
```

---

# 53. Final Mental Model

The whole system can be understood using four questions:

```text
What are the things?
```

```text
MenuItem
Restaurant
User
Cart
Order
```

```text
What behavior changes?
```

```text
Payment Strategy
```

```text
What objects need different creation logic?
```

```text
Order Factory
```

```text
What objects are globally managed?
```

```text
RestaurantManager
OrderManager
```

And finally:

```text
Who coordinates everything?
```

```text
Tomato
```

The architecture is therefore:

```text
DOMAIN OBJECTS
    |
    v
BEHAVIOR ABSTRACTION
    |
    v
ORDER HIERARCHY
    |
    v
OBJECT CREATION
    |
    v
OBJECT MANAGEMENT
    |
    v
NOTIFICATION
    |
    v
APPLICATION ORCHESTRATION
```

This gives a clean dependency-first way to read and implement the system.
