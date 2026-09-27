from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """
    Strategy Interface for all payment methods.

    All payment types must implement pay().
    """

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

"""
CheckoutService
      ↓
PaymentStrategy (interface)
      ↓
[UPI | Card | Wallet | COD]

"""