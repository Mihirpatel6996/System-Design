from abc import ABC, abstractmethod 

class PaymentGateway(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

class Stripe(PaymentGateway):
    def pay(self, amount):
        ## logic of stripe payment gateway
        print("Processing via Stripe")

class Razorpay(PaymentGateway):
    def pay(self, amount):
        ## logic of razorpay payment gateway
        print("Processing via Razorpay")


## my system 

def process_payment(gateway: PaymentGateway, amount):
    gateway.pay(amount)

## usage of the sytem 

process_payment(Stripe(), 100)  ## this will work fine because Stripe class implements the pay method defined in the PaymentGateway abstract class


process_payment(Razorpay(), 200)  ## this will work fine because Razorpay class implements the pay method defined in the PaymentGateway abstract class



