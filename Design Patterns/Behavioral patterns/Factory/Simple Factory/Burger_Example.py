# Define Base Class
from abc import ABC, abstractmethod

# priduct Interface
class Burger(ABC):
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

# Factory Class

class BurgerFactory:
    def create_burger(self, burger_type: str) -> Burger:
        if burger_type == "basic":
            return BasicBurger()
        elif burger_type == "standard":
            return StandardBurger()
        elif burger_type == "premium":
            return PremiumBurger()
        else:
            raise ValueError("Invalid burger type")

# Client Code
if __name__ == "__main__":
    burger_type = "standard"

    factory = BurgerFactory()

    burger = factory.create_burger(burger_type)

    burger.prepare()

'''
What Changed:

Without Factory : client directly creates the burger object, leading to tight coupling and less flexibility. The client needs to know about the concrete classes and their instantiation.

Client --> directly creates objects 

with factory : client uses the factory to create the burger object, promoting loose coupling and flexibility. The client only needs to know about the factory and the abstract class, not the concrete implementations.

client -> factory -> creats objects


'''

'''
Identify Components (important for interviews)
    Factory → BurgerFactory
    Product Interface → Burger
    Concrete Products → BasicBurger, StandardBurger, PremiumBurger
    Client → main function
'''

