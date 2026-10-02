What actually happens (Execution Trace)
Now we expand the full runtime flow.
STEP 1 → Notification creation (Decorator chain)
SimpleNotification("Order shipped")
        ↓
TimestampDecorator
        ↓
SignatureDecorator

Final object:
"[timestamp] Order shipped\n-- Customer Care Team"

STEP 2 → Service entry point
service.send_notification(notification)

Inside service:
1. store notification
2. observable.set_notification(notification)

STEP 3 → Observable triggers event
set_notification()
    → notify_observers()

Observers list:
- Logger
- NotificationEngine
STEP 4 → Logger executes first
Logger.update()
    → fetch notification
    → print log

Output:
[LOGGER] New Notification Received:
[timestamp] Order shipped
-- Customer Care Team

STEP 5 → NotificationEngine executes
NotificationEngine.update()
    → get_notification()
    → get_content()

Now decorator chain re-executes:
SignatureDecorator
    → TimestampDecorator
        → SimpleNotification

Final content produced.
STEP 6 → Strategy execution
Engine loops through strategies:
EmailStrategy.send()
SMSStrategy.send()
PopupStrategy.send()

Output:
[EMAIL] Sending to user@example.com
[timestamp] Order shipped
-- Customer Care Team

[SMS] Sending to +91-9876543210
[timestamp] Order shipped
-- Customer Care Team

[POPUP] Displaying in app:
[timestamp] Order shipped
-- Customer Care Team

Final System View (Mental Model)
Client
  ↓
NotificationService (Singleton)
  ↓
NotificationObservable
  ↓
Observers:
   ├── Logger
   └── NotificationEngine
                 ↓
          Notification (Decorators)
                 ↓
        Strategy Layer
   ┌────────┬────────┬────────┐
   ↓        ↓        ↓
 Email     SMS     Popup

What you have actually built
This is not “design patterns practice”.
This is a mini event-driven notification platform:
You implemented:
- Content pipeline (Decorator)
- Event system (Observer)
- Delivery system (Strategy)
- Global orchestration (Singleton)
Real-world mapping
This architecture maps to production systems like:
- Amazon notification system
- Uber trip updates
- Swiggy/Zomato order updates
- Banking alert systems
Critical engineering insight (important)
Right now everything is:
Synchronous + in-memory + tightly coupled execution

So at scale, you would evolve into:
Observable → Kafka topic
Engine → Worker service
Strategies → microservices

Decorators still stay (message enrichment layer).