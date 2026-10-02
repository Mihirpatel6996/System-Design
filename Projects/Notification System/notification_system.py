# Notification Interface

from abc import ABC, abstractmethod
from typing import Optional


class Notification(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


# Concrete Notification Classes

class SimpleNotification(Notification):
    def __init__(self, text: str):
        self.text = text

    def get_content(self) -> str:
        return self.text

"""
Problem
We want to add behavior to a notification dynamically, like:
    - Add timestamp
    - Add signature
    - Add priority tag
    - Add formatting
But without:
    - Modifying SimpleNotification
    - Creating 100 subclasses like:
        - TimestampNotification
        - SignatureNotification
        - TimestampSignatureNotification
        - etc. (combinatorial explosion)

So we will use the Decorator Pattern to achieve this.
"""

# Decorator Base class / Wrapper class

class NotificationDecorator(Notification):
    def __init__(self, notification: Notification):
        self._notification = notification

    def get_content(self) -> str:
        return self._notification.get_content()

"""
What did we do here?
--> This class implements the Notification and contains a reference to another Notification object., Thats the trick.
"""

# Concrete Decorators

# 1. Timestamp Decorator

from datetime import datetime


class TimestampDecorator(NotificationDecorator):
    def get_content(self) -> str:
        original_content = self._notification.get_content()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {original_content}"

"""
Execution Flow :

n = SimpleNotification("Order shipped")
n = TimestampDecorator(n)

print(n.get_content())

        TimestampDecorator.get_content()
            → calls SimpleNotification.get_content()
                → returns "Order shipped"
            → adds timestamp
            → returns "[time] Order shipped"

"""

# 2. Signature Decorator

class SignatureDecorator(NotificationDecorator):
    def __init__(self, notification: Notification, signature: str):
        super().__init__(notification)
        self.signature = signature

    def get_content(self) -> str:
        original_content = self._notification.get_content()
        return f"{original_content}\n-- {self.signature}"

"""
Execution Flow :

n = SimpleNotification("Your order has been shipped!")
n = TimestampDecorator(n)
n = SignatureDecorator(n, "Customer Care")

print(n.get_content())

SignatureDecorator.get_content()
    → calls TimestampDecorator.get_content()
        → calls SimpleNotification.get_content()
            → returns "Your order has been shipped!"
        → adds timestamp
        → returns "[time] Your order has been shipped!"
    → adds signature
    → returns:
        "[time] Your order has been shipped!
         -- Customer Care"

"""

"""
Lets now move on to observable pattern, which will allow us to notify multiple observers when a notification is sent.
"""

# 1. define the Observer interface

from abc import ABC, abstractmethod


class NotificationObserver(ABC):
    @abstractmethod
    def update(self):
        pass

# 2. define the Observable interface

class NotificationObservable(ABC):

    @abstractmethod
    def add_observer(self, observer: NotificationObserver) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: NotificationObserver) -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass

    @abstractmethod
    def set_notification(self, notification: Notification) -> None:
        pass

    @abstractmethod
    def get_notification(self) -> Optional[Notification]:
        pass

    @abstractmethod
    def get_notification_content(self) -> str:
        pass


# 3. define the concrete Observable class

class NotificationObservable:
    def __init__(self):
        self._observers = []
        self._current_notification: Notification | None = None

    def add_observer(self, observer: NotificationObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: NotificationObserver):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

    def set_notification(self, notification: Notification):
        self._current_notification = notification
        self.notify_observers()

    def get_notification(self) -> Notification:
        return self._current_notification

    def get_notification_content(self) -> str:
        return self._current_notification.get_content()


# defining concrete observer classes

class Logger(NotificationObserver):
    def __init__(self, observable: NotificationObservable):
        self._observable = observable
        self._observable.add_observer(self)

    def update(self) -> None:
        notification = self._observable.get_notification()
        content = notification.get_content() if notification else "No notification"
        print(f"[LOGGER] New Notification Received:\n{content}\n")


'''
Now we move into the delivery layer abstraction.
    Until now:
        - Decorator → changes content
        - Observer → reacts to event
    Now we add:
        - Strategy → decides how to deliver
    This is the third axis of our system.
'''


"""
    Same notification content can be delivered in multiple ways:
    - Email
    - SMS
    - Push notification
    - WhatsApp (future)
    - In-app popup
"""

# NotificationStrategy (Abstract Base Class)

class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, content: str) -> None:
        pass

# Concrete Strategies

#1. EmailNotificationStrategy

class EmailStrategy(NotificationStrategy):
    def __init__(self, email_id: str):
        self.email_id = email_id

    def send(self, content: str) -> None:
        print(f"[EMAIL] Sending to {self.email_id}")
        print(f"Content:\n{content}\n")

#2. SMSNotificationStrategy
class SMSStrategy(NotificationStrategy):
    def __init__(self, mobile_number: str):
        self.mobile_number = mobile_number

    def send(self, content: str) -> None:
        print(f"[SMS] Sending to {self.mobile_number}")
        print(f"Content:\n{content}\n")

#3. PushNotificationStrategy
class PopupStrategy(NotificationStrategy):
    def send(self, content: str) -> None:
        print(f"[POPUP] Displaying in app:")
        print(content)

"""
NotificationEngine (VERY IMPORTANT) -->concrete class that integrates Observer and Strategy patterns
    Now we build the glue:
    Observer + Strategy integration point
        This is where:
            - event comes in
            - strategies are selected
            - delivery happens

"""

"""
Problem : 
We need a component that:
    - Listens to notification events (Observer)
    - Fetches notification content
    - Sends it through multiple delivery channels (Strategy)
So it becomes the execution layer of the system.
"""

class NotificationEngine(NotificationObserver):

    def __init__(self, observable: NotificationObservable):
        self._observable = observable
        self._observable.add_observer(self)
        self._strategies: list[NotificationStrategy] = []

    def add_strategy(self, strategy: NotificationStrategy):
        self._strategies.append(strategy)

    def update(self) -> None:
        notification = self._observable.get_notification()

        if not notification:
            return

        content = notification.get_content()

        for strategy in self._strategies:
            strategy.send(content)


"""
Perfect !!!!

What you just built (important)
    we now have a 3-layer notification system:
        1. Data Layer (Decorator)
        - builds message
        2. Event Layer (Observer)
        - triggers reaction
        3. Delivery Layer (Strategy)
        - sends message
"""

"""
What works well here
    1. Extensibility
    we can add:
        - WhatsAppStrategy
        - SlackStrategy
        - PushNotificationStrategy
    without touching engine

    2. Separation of concerns
        - Engine doesn’t know how email works
        - Strategy doesn’t know who triggered event
        - Decorator doesn’t know delivery channels

        

"""
# final step

"""
We need a single entry point for the entire system.
Why?
Because without it:
    - multiple observables can exist → inconsistent state
    - observers get wired incorrectly
    - engine setup becomes scattered across codebase
So this becomes the composition root of your system.


So we will create a NotificationSystem class -- Singleton Design Pattern

It is responsible for:
1. Creating observable
2. Exposing observable to system
3. Sending notifications
4. Acting as singleton (single control plane)

"""

# implementation

class NotificationService:
    _instance = None

    def __init__(self):
        self._observable = NotificationObservable()
        self._notifications = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NotificationService()
        return cls._instance

    def get_observable(self) -> NotificationObservable:
        return self._observable

    def send_notification(self, notification: Notification) -> None:
        self._notifications.append(notification)
        self._observable.set_notification(notification)


# client code 

if __name__ == "__main__":

    # 1. Get singleton service
    service = NotificationService.get_instance()

    # 2. Create observers
    logger = Logger(service.get_observable())

    engine = NotificationEngine(service.get_observable())

    # 3. Register delivery strategies
    engine.add_strategy(EmailStrategy("user@example.com"))
    engine.add_strategy(SMSStrategy("+91-9876543210"))
    engine.add_strategy(PopupStrategy())

    # 4. Build notification using decorators
    notification: Notification = SimpleNotification(
        "Your order has been shipped!"
    )

    notification = TimestampDecorator(notification)
    notification = SignatureDecorator(notification, "Customer Care Team")

    # 5. Send notification (single entry point)
    service.send_notification(notification)
    



    








