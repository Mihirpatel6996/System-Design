1. Problem (real-world framing)
Imagine you are building a notification system.
You have a base service:
Send a notification (email/message)

But now requirements grow:
- log every notification
- encrypt message
- retry failed sends
- add timestamp
- send SMS copy
Now ask:
Do you create 20 subclasses like LoggedEncryptedRetryNotification?

No. That explodes like Mario did.
So we use Decorator.
2. Naive implementation (WITHOUT decorator)
class NotificationService:    def send(self, message: str):        print(f"Sending: {message}")


Now you try extending behavior:
class LoggedNotificationService(NotificationService):    def send(self, message: str):        print("[LOG] Sending notification")        return super().send(message)class EncryptedNotificationService(NotificationService):    def send(self, message: str):        encrypted = f"ENCRYPTED({message})"        return super().send(encrypted)


Problem here
If you want both logging + encryption:
LoggedEncryptedNotificationService ❌
EncryptedLoggedNotificationService ❌
LoggedEncryptedRetryNotificationService ❌

Explosion again.


