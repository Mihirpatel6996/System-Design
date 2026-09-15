## you are building a payment system -- that accepts multiple payment methods (e.g., credit card, PayPal, bank transfer).

class PaymentProcessor:

    def process(self, payment_type, amount):

        if payment_type == "credit_card":
            return f"Processing credit card payment of {amount}"

        elif payment_type == "upi":
            return f"Processing UPI payment of {amount}"

        elif payment_type == "paypal":
            return f"Processing PayPal payment of {amount}"

        else:
            raise ValueError("Unsupported payment type")

# now for every new payment method we have to modify the existing PaymentProcessor class which violates the open closed principle.

# at real scale 15+ payment methods are added every month. So every time we have to modify the existing class which is not a good design.

# class will have now 500 + lines of code and will be very hard to maintain.

# apply OCP --> use abstraction - one interface and multiple implementations

# Refer OCP_Example_2.py for solution
