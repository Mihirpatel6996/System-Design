from typing import List, Optional
from models.restaurant import Restaurant


class RestaurantManager:
    """
    Singleton Service Layer for managing restaurants.

    Responsibilities:
    - Store restaurants in memory
    - Provide search APIs
    """

    _instance: Optional["RestaurantManager"] = None

    def __init__(self):
        # In-memory storage (acts like a DB table)
        self._restaurants: List[Restaurant] = []

    # ---------------- Singleton Access ----------------
    @classmethod
    def get_instance(cls) -> "RestaurantManager":
        if cls._instance is None:
            cls._instance = RestaurantManager()
        return cls._instance

    # ---------------- Business Methods ----------------

    def add_restaurant(self, restaurant: Restaurant) -> None:
        self._restaurants.append(restaurant)

    def search_by_location(self, location: str) -> List[Restaurant]:
        """
        Returns all restaurants matching location (case-insensitive exact match)
        """
        location = location.lower()

        result = []
        for restaurant in self._restaurants:
            if restaurant.get_location().lower() == location:
                result.append(restaurant)

        return result

'''
# prolems here 

1. no persistant
2. no validation  -- user can add null resturant or empty name or location
3. linear search (time complexity O(n))
4. no concurrency saftey in singleton class
    '''