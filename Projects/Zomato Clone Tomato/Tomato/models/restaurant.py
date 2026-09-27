from typing import List
from models.menu_items import MenuItem


class Restaurant:
    """
    Represents a restaurant in the food ordering system.

    Responsibilities:
    - Holds restaurant metadata
    - Owns menu items
    """

    # class-level variable (simulating static in Java)
    _next_restaurant_id = 0

    def __init__(self, name: str, location: str):
        Restaurant._next_restaurant_id += 1
        self._restaurant_id = Restaurant._next_restaurant_id

        self._name = name
        self._location = location

        # aggregation relationship: Restaurant HAS MenuItems
        self._menu: List[MenuItem] = []

    # ---------------- getters/setters ----------------

    def get_restaurant_id(self) -> int:
        return self._restaurant_id

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_location(self) -> str:
        return self._location

    def set_location(self, location: str) -> None:
        self._location = location

    # ---------------- menu operations ----------------

    def add_menu_item(self, item: MenuItem) -> None:
        """
        Adds a menu item to the restaurant menu.
        In real systems, this would also:
        - update cache
        - update search index
        - trigger event
        """
        self._menu.append(item)

    def get_menu(self) -> List[MenuItem]:
        return self._menu

    # ---------------- debug ----------------

    def __repr__(self) -> str:
        return f"Restaurant(id={self._restaurant_id}, name={self._name}, location={self._location})"