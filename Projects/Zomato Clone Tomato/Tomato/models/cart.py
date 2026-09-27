from typing import List, Optional
from models.menu_items import MenuItem
from models.restaurant import Restaurant


class Cart:
    """
    Cart represents a temporary order before checkout.

    Key constraint:
    - A cart can belong to ONLY ONE restaurant at a time
    """

    def __init__(self):
        self._restaurant: Optional[Restaurant] = None
        self._items: List[MenuItem] = []

    # ---------------- Restaurant binding ----------------

    def set_restaurant(self, restaurant: Restaurant) -> None:
        """
        Locks cart to a single restaurant.
        Once set, all items must belong to same restaurant.
        """
        self._restaurant = restaurant

    def get_restaurant(self) -> Optional[Restaurant]:
        return self._restaurant

    # ---------------- Cart operations ----------------

    def add_item(self, item: MenuItem) -> None:
        """
        Adds item to cart.

        Constraint:
        - Cannot add items before selecting restaurant
        """
        if self._restaurant is None:
            print("Cart Error: Set a restaurant before adding items.")
            return

        self._items.append(item)

    def get_items(self) -> List[MenuItem]:
        return self._items

    # ---------------- Business logic ----------------

    def get_total_cost(self) -> float:
        """
        Aggregates total price of all items in cart
        """
        total = 0
        for item in self._items:
            total += item.get_price()
        return total

    def is_empty(self) -> bool:
        return self._restaurant is None or len(self._items) == 0

    def clear(self) -> None:
        """
        Resets cart completely (new session behavior)
        """
        self._items.clear()
        self._restaurant = None

# problems here
'''
1. No validation of item-restaurant mismatch 
2. No persistence (cart is in-memory only)
3. No concurrency safety (if used in multi-threaded environment)
4. Complexity Analysis - O(n) for adding items, O(1) for getting total cost
'''