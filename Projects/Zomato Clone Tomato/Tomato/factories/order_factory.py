from abc import ABC, abstractmethod
from typing import List

from models.user import User
from models.cart import Cart
from models.restaurant import Restaurant
from models.menu_items import MenuItem
from models.orders import Order
from strategies.payment_strategy import PaymentStrategy


class OrderFactory(ABC):
    """
    Abstract Factory for creating Orders.
    """

    @abstractmethod
    def create_order(
        self,
        user: User,
        cart: Cart,
        restaurant: Restaurant,
        items: List[MenuItem],
        payment_strategy: PaymentStrategy,
        order_type: str
    ) -> Order:
        pass