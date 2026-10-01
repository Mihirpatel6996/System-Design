Very Very Important : I’ll use the notification decorator example because it is closer to real systems than Mario.
1. Final code we are executing
service = EmailNotification()service = LoggingDecorator(service)service = EncryptionDecorator(service)service = RetryDecorator(service)service.send("Payment successful")


2. Key idea before execution
At this point, memory looks like this:
service
  ↓
RetryDecorator( EncryptionDecorator( LoggingDecorator( EmailNotification ) ) )

So the object is:
RetryDecorator object
    has LoggingDecorator
        has EncryptionDecorator
            has EmailNotification

3. Now execution starts
We call:
service.send("Payment successful")


But IMPORTANT:
👉 service is NOT EmailNotification anymore
👉 it is RetryDecorator
So first call goes here:
4. Step-by-step execution flow (VERY IMPORTANT)
STEP 1 — RetryDecorator
class RetryDecorator(NotificationDecorator):    def send(self, message: str):        try:            return self.notification.send(message)


So execution enters:
RetryDecorator.send("Payment successful")

Now it does:
self.notification.send(message)


But what is self.notification?
👉 It is EncryptionDecorator
So next call goes there.
STEP 2 — EncryptionDecorator
class EncryptionDecorator(NotificationDecorator):    def send(self, message: str):        encrypted = f"ENCRYPTED({message})"        return self.notification.send(encrypted)


So now:
EncryptionDecorator.send("Payment successful")

It transforms message:
"Payment successful"
→ "ENCRYPTED(Payment successful)"

Then calls next layer:
self.notification.send(encrypted)


👉 Next layer = LoggingDecorator
STEP 3 — LoggingDecorator
class LoggingDecorator(NotificationDecorator):    def send(self, message: str):        print(f"[LOG] Sending message: {message}")        return self.notification.send(message)


Now:
LoggingDecorator.send("ENCRYPTED(Payment successful)")

It does:
[LOG] Sending message: ENCRYPTED(Payment successful)

Then calls next:
self.notification.send(message)


👉 Next = EmailNotification
STEP 4 — EmailNotification (base)
class EmailNotification(Notification):    def send(self, message: str):        print(f"Email sent: {message}")


Now:
EmailNotification.send("ENCRYPTED(Payment successful)")

Output:
Email sent: ENCRYPTED(Payment successful)

5. Now unwind (VERY IMPORTANT concept)
Execution returns back step by step:
EmailNotification returns
→ LoggingDecorator returns
→ EncryptionDecorator returns
→ RetryDecorator returns

So final output:
[LOG] Sending message: ENCRYPTED(Payment successful)
Email sent: ENCRYPTED(Payment successful)

6. Full execution stack (VISUAL)
Here is the full call chain:
service.send()
    ↓
RetryDecorator.send()
    ↓
EncryptionDecorator.send()
    ↓
LoggingDecorator.send()
    ↓
EmailNotification.send()

Then return goes back up.
7. Why this feels confusing
Because there are TWO flows:
(A) Construction flow (wrapping)
Email → Logging → Encryption → Retry

This is INSIDE-OUT creation.
(B) Execution flow (calling)
Retry → Encryption → Logging → Email

This is OUTSIDE-IN execution.
8. Mental model (THIS is the key)
Think of decorators like a stack:
PUSH (wrapping)
Email
push Logging
push Encryption
push Retry

POP (execution)
Retry → Logging → Encryption → Email

9. One-line summary
Decorator builds a stack of objects, and execution flows top → bottom, then returns bottom → top.

10. If you still feel unclear, ask yourself this
When you see:
service = LoggingDecorator(service)


Ask:
- What is inside service now?
- Who is actually holding the real EmailNotification?
- Which layer is outermost?