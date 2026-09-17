from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailNotification(Notification):
    def send(self, message):
        print(f"Email sent: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS sent: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"Push sent: {message}")


class SilentNotification(Notification):
    def send(self, message):
        raise Exception("Silent mode does not send messages")

## why this is wrong -> It violates the Liskov Substitution Principle because it changes the behavior of the parent class in a way that breaks the expected contract.

def notify_user(notification: Notification, message: str):
    notification.send(message)

notify_user(EmailNotification(), "Hello via Email!")  # works
notify_user(SMSNotification(), "Hello via SMS!")  # works
notify_user(PushNotification(), "Hello via Push!")  # works
notify_user(SilentNotification(), "Hello!")  #  raises Exception



