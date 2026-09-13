# Dynamc Dipatch / Runtime Polymorphism / method overriding

class Notification:
    def send(self, message):
        print("Base notification")


class EmailNotification(Notification):
    def send(self, message):
        print(f"Email: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS: {message}")


#Now : 

def notify(notification):
    notification.send("Hello")

#usage -> this will call the send method of the appropriate class based on the object type passed to it at runtime

notify(EmailNotification())
notify(SMSNotification())


