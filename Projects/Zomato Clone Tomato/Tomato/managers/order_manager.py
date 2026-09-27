from typing import List, Optional

from models.orders import Order


class OrderManager:
    """
    Singleton service for managing orders.

    Responsibilities:
    - Store orders (in-memory for now)
    - Provide listing/visibility
    """

    _instance: Optional["OrderManager"] = None

    def __init__(self):
        self._orders: List[Order] = []

    # ---------------- Singleton ----------------

    @classmethod
    def get_instance(cls) -> "OrderManager":
        if cls._instance is None:
            cls._instance = OrderManager()
        return cls._instance

    # ---------------- Core operations ----------------

    def add_order(self, order: Order) -> None:
        """
        Adds a new order to the system.
        """
        self._orders.append(order)

    def list_orders(self) -> None:
        """
        Prints all orders (debug/CLI view).
        """
        print("\n--- All Orders ---")

        for order in self._orders:
            user = order.get_user()
            user_name = user.get_name() if user else "Unknown"

            print(
                f"{order.get_type()} order for {user_name} "
                f"| Total: ₹{order.get_total()} "
                f"| At: {order.get_scheduled()}"
            )