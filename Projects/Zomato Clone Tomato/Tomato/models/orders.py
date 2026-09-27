from abc import ABC, abstractmethod
from typing import List, Optional

from models.user import User
from models.restaurant import Restaurant
from models.menu_items import MenuItem
from strategies.payment_strategy import PaymentStrategy


class Order(ABC):
    """
    Abstract Order class.

    Represents a finalized or in-progress order in the system.
    """

    _next_order_id = 0

    def __init__(self):
        Order._next_order_id += 1

        self._order_id: int = Order._next_order_id
        self._user: Optional[User] = None
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []

        self._payment_strategy: Optional[PaymentStrategy] = None

        self._total: float = 0.0
        self._scheduled: str = ""

    # ---------------- core business logic ----------------

    def process_payment(self) -> bool:
        """
        Delegates payment to strategy.
        """
        if self._payment_strategy is None:
            print("Please choose a payment mode first")
            return False

        self._payment_strategy.pay(self._total)
        return True

    # ---------------- abstract ----------------

    @abstractmethod
    def get_type(self) -> str:
        pass

    # ---------------- getters ----------------

    def get_order_id(self) -> int:
        return self._order_id

    def get_user(self) -> Optional[User]:
        return self._user

    def get_restaurant(self) -> Optional[Restaurant]:
        return self._restaurant

    def get_items(self) -> List[MenuItem]:
        return self._items

    def get_total(self) -> float:
        return self._total

    def get_scheduled(self) -> str:
        return self._scheduled

    # ---------------- setters ----------------

    def set_user(self, user: User) -> None:
        self._user = user

    def set_restaurant(self, restaurant: Restaurant) -> None:
        self._restaurant = restaurant

    def set_items(self, items: List[MenuItem]) -> None:
        """
        Sets items and recalculates total.

        IMPORTANT:
        This is a snapshot operation (very important in real systems)
        """
        self._items = items
        self._total = sum(item.get_price() for item in items)

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy

    def set_scheduled(self, scheduled: str) -> None:
        self._scheduled = scheduled

    def set_total(self, total: float) -> None:
        self._total = total
