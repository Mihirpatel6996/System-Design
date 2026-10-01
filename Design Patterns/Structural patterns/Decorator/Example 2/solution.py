# component Interface

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

# core component implementation 
class EmailNotification(Notification):
    def send(self, message: str):
        print(f"Email sent: {message}")


# Decorator base class

class NotificationDecorator(Notification):
    def __init__(self, notification: Notification):
        self.notification = notification

    def send(self, message: str):
        return self.notification.send(message)


# concrete decorators

class LoggingDecorator(NotificationDecorator):
    def send(self, message: str):
        print(f"[LOG] Sending message: {message}")
        return self.notification.send(message)

# Encryption Decorators

class EncryptionDecorator(NotificationDecorator):
    def send(self, message: str):
        encrypted = f"ENCRYPTED({message})"
        return self.notification.send(encrypted)


# Retry Decorator

class RetryDecorator(NotificationDecorator):
    def send(self, message: str):
        try:
            return self.notification.send(message)
        except Exception:
            print("Retrying...")
            return self.notification.send(message)


# # Client code
# service = RetryDecorator(EncryptionDecorator(LoggingDecorator(EmailNotification())))
# service.send("Payment successful")

service = EmailNotification()

service = LoggingDecorator(service)
service = EncryptionDecorator(service)
service = RetryDecorator(service)

service.send("Payment successful")

