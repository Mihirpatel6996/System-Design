'''
You’re building a clinical AI pipeline (very close to your MIMIC system):

Kafka → Consumer → Process Vitals → Store → Generate Alert → Notify → Log

Now imagine you write everything in one class.

'''


class PatientMonitor:

    def __init__(self, db):
        self.db = db

    def consume_kafka(self, message):
        # simulate message consumption
        return message

    def process_vitals(self, data):
        # business logic
        hr = data["heart_rate"]
        if hr > 120:
            return "HIGH_RISK"
        return "NORMAL"

    def save_to_db(self, patient_id, status):
        print(f"Saving {patient_id} → {status}")
        # pretend DB write

    def send_alert(self, patient_id, status):
        if status == "HIGH_RISK":
            print(f"ALERT sent for {patient_id}")

    def log(self, message):
        print(f"LOG: {message}")

    def run(self, message):
        data = self.consume_kafka(message)
        status = self.process_vitals(data)
        self.save_to_db(data["patient_id"], status)
        self.send_alert(data["patient_id"], status)
        self.log("Processed successfully")



# Stop and think here 

# 1. how many reasons to change does this class have?
# 2. how many different responsibilities does this class have?
# 3.What happens if alerting moves from email → WhatsApp → PagerDuty?
# 4.What if DB changes from Postgres → Cassandra?
# 5.What if logging moves to Kafka-based centralized logging?
# 6.What if we want to reuse processing logic in batch jobs?

# so many reasons to change, so many responsibilities. This is a textbook violation of the Single Responsibility Principle (SRP).

# srp says that a class should have only one reason to change. In this case, the PatientMonitor class has multiple reasons to change: changes in alerting mechanism, database technology, logging system, and processing logic. Each of these responsibilities should be separated into different classes or modules to adhere to SRP and make the code more maintainable and flexible.
