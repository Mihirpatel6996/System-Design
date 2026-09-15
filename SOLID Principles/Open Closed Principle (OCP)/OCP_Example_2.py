# create abstraction

from abc import ABC, abstractmethod

class PaymentMethod(ABC):

    @abstractmethod
    def process(self, amount):
        pass


# concrete implementations

class CreditCardPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing credit card payment of {amount}"

class UPIPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing UPI payment of {amount}"

class PayPalPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing PayPal payment of {amount}"


# closed for modification

class PaymentProcessor:

    def process(self, payment_method: PaymentMethod, amount):
        return payment_method.process(amount)

# now if the product says add crypto payments just do 

class CryptoPayment(PaymentMethod):

    def process(self, amount):
        return f"Processing crypto payment of {amount}" 


