from model import PaymentRequest
from payment_gateway import PaymentGateway
from payment_gateway_proxy import PaymentGatewayProxy
from enum import GatewayType
from payment_gateway import PaytmGateway, RazorpayGateway
from payment_gateway_factory import GatewayFactory


class PaymentService:

    def process_payment(
        self,
        gateway: PaymentGateway,
        request: PaymentRequest
    ) -> bool:

        print("[PaymentService] Processing payment request")

        return gateway.process_payment(request)