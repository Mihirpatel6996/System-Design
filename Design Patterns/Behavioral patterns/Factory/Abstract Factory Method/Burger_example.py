'''
But if i want to add a new burger type, I will have to modify all the existing factory classes to handle the new burger type. This is a limitation of the factory method pattern, as it does not fully adhere to the Open/Closed Principle when it comes to adding new product types.

solution - abstract factory pattern
'''

# Product Interface

from abc import ABC, abstractmethod

class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


class GarlicBread(ABC):
    @abstractmethod
    def prepare(self):
        pass

# Concrete Classes/products

class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


class BasicGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Basic Garlic Bread with butter and garlic!")


class CheeseGarlicBread(GarlicBread):
    def prepare(self):
        print("Preparing Cheese Garlic Bread with extra cheese and butter!")