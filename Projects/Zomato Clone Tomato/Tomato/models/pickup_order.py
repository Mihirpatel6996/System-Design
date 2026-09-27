from models.orders import Order


class PickupOrder(Order):
    """
    Represents a self-pickup order.

    User will collect order from restaurant.
    """

    def __init__(self):
        super().__init__()
        self._restaurant_address: str = ""

    def get_type(self) -> str:
        return "Pickup"

    # ---------------- pickup-specific ----------------

    def set_restaurant_address(self, address: str) -> None:
        self._restaurant_address = address

    def get_restaurant_address(self) -> str:
        return self._restaurant_address