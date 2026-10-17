from payment_gateway_factory import GatewayFactory
from payment_service import PaymentService
from payment_controller import PaymentController
from enum import GatewayType
from model import PaymentRequest



factory = GatewayFactory()
service = PaymentService()
controller = PaymentController(service, factory)

request = PaymentRequest(
    sender="Aditya",
    receiver="Shubham",
    amount=1000,
    currency="INR"
)

result = controller.handle_payment(
    GatewayType.PAYTM,
    request
)

print("FINAL RESULT:", result)



"""
client --> controller --> service --> factory --> gateway --> banking system


User (Client)
    ↓
Waiter (Controller)
    ↓
Manager (Service)
    ↓
Supplier Selector (Factory)
    ↓
Chef Recipe (Gateway)
    ↓
Kitchen Infrastructure (BankingSystem)



"""