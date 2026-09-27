class MenuItem:
    """
    Represents a single item in a restaurant menu.

    This is a simple data model used across the system:
    - Restaurant contains MenuItems
    - Cart contains MenuItems
    - Order references MenuItems
    """

    def __init__(self, code: str, name: str, price: int):
        self._code = code
        self._name = name
        self._price = price

    # ---------- getters ----------
    def get_code(self) -> str:
        return self._code

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> int:
        return self._price

    # ---------- setters ----------
    def set_code(self, code: str) -> None:
        self._code = code

    def set_name(self, name: str) -> None:
        self._name = name

    def set_price(self, price: int) -> None:
        self._price = price

    # ---------- debug helper ----------
    def __repr__(self) -> str:
        return f"MenuItem(code={self._code}, name={self._name}, price={self._price})"

    
'''
What breaks at scale?
Right now:
    Problem 1: No validation
        - Negative price allowed
        - Empty name allowed
    Problem 2: No immutability
        - MenuItem can be changed after being added to:
        - cart
        - order history (BAD in real systems)
    Problem 3: No versioning
        - Restaurants update menu → old orders break consistency assumptions

'''