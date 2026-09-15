# Break into components 

class KafkaConsumer:
    def consume(self, message):
        return message

class VitalsProcessor:
    def process(self, data):
        hr = data["heart_rate"]
        return "HIGH_RISK" if hr > 120 else "NORMAL"

class PatientRepository:
    def save(self, patient_id, status):
        print(f"Saving {patient_id} → {status}")

class AlertService:
    def send(self, patient_id, status):
        if status == "HIGH_RISK":
            print(f"ALERT sent for {patient_id}")

class Logger:
    def log(self, message):
        print(f"LOG: {message}")


# Main class that orchestrates the components

class PatientMonitorService:

    def __init__(self, consumer, processor, repo, alert, logger):
        self.consumer = consumer
        self.processor = processor
        self.repo = repo
        self.alert = alert
        self.logger = logger

    def run(self, message):
        data = self.consumer.consume(message)
        status = self.processor.process(data)
        self.repo.save(data["patient_id"], status)
        self.alert.send(data["patient_id"], status)
        self.logger.log("Processed successfully")

