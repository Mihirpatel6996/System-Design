from models.cart import Cart


class User:
    """
    Represents a system user.

    Responsibilities:
    - Owns a cart (current session order builder)
    - Holds identity + delivery info
    """

    def __init__(self, user_id: int, name: str, address: str):
        self._user_id = user_id
        self._name = name
        self._address = address

        # Each user has exactly one active cart (simple model)
        self._cart = Cart()

    # ---------------- getters/setters ----------------

    def get_user_id(self) -> int:
        return self._user_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_address(self) -> str:
        return self._address

    def set_address(self, address: str) -> None:
        self._address = address

    # ---------------- cart access ----------------

    def get_cart(self) -> Cart:
        return self._cart

    def __repr__(self) -> str:
        return f"User(id={self._user_id}, name={self._name})"
