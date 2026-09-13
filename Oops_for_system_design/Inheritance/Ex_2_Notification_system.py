'''
Practice task

Implement:

Base class

Notification
    send(message)

Child classes
EmailNotification
SMSNotification
PushNotification

Each:

implements send differently
optionally reuse shared logging from parent


What I will check
Did you use inheritance only for “is-a”
Did you avoid forcing relationships
Did you use overriding properly
Did you avoid unnecessary coupling
'''


from abc import ABC, abstractmethod
from email.mime import base

class Notification(ABC):
    
    @abstractmethod
    def send(self, message):
        pass

    def log(self, message):
        print(f"[LOG]: {message}")

class EmailNotification(Notification):
    def send(self, message):
        self.log(f"Sending email: {message}")
        self.log(f"Email sent: {message}") # Reuse the log method from the parent class
        print(f"Email sent: {message}")


class SMSNotification(Notification):
    def send(self, message):
        self.log(f"Sending SMS: {message}")
        self.log(f"SMS sent: {message}")  # Reuse the log method from the parent class
        print(f"SMS sent: {message}")


class PushNotification(Notification):
    def send(self, message):
        self.log(f"Sending push notification: {message}")
        self.log(f"Push notification sent: {message}")  # Reuse the log method from the parent class
        print(f"Push notification sent: {message}")


## Learning points
# 1. Inheritance is used to create a base class Notification that defines the interface for sending notifications. The child classes EmailNotification, SMSNotification, and PushNotification inherit from the base class and provide their own implementations of the send method.
# 2. The log method is defined in the base class and is reused in the child classes to log messages related to sending notifications. This demonstrates code reuse through inheritance.
# 3. The design follows the "is-a" relationship, where each notification type is a type of Notification. This allows for polymorphism, enabling the use of different notification types interchangeably.
# 4. The design avoids unnecessary coupling by keeping the notification types independent of each other. Each notification type can be used without relying on the implementation details of the others.
# 5. The use of abstract base classes (ABC) and abstract methods enforces that any subclass must implement the send method, ensuring that all notification types adhere to the same interface.






