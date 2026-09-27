from models.orders import Order


class DeliveryOrder(Order):
    """
    Represents a delivery order.

    Food is delivered to user's address.
    """

    def __init__(self):
        super().__init__()
        self._user_address: str = ""

    def get_type(self) -> str:
        return "Delivery"

    # ---------------- delivery-specific ----------------

    def set_user_address(self, address: str) -> None:
        self._user_address = address

    def get_user_address(self) -> str:
        return self._user_address