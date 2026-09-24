# In simple factory we have seen the factory --> BurgerFactory handles the creation of burger objects. Now if we want to add a new type of burger, we would have to modify the BurgerFactory class, which violates the Open/Closed Principle.

#  In factory method pattern, we will have a separate factory for each type of burger. This allows for more flexibility and adheres to the Open/Closed Principle, as new burger types can be added without modifying existing code.

# Factory Method defines an interface for creating an object, but lets subclasses decide which concrete class to instantiate.

# Client → Abstract Factory → Concrete Factory → Product

## Problem statement: Now we have 2 dimensions Burger type and Restaurant. If we keep using the simple factory pattern, we would have to create a new method in the factory for each combination of burger type and restaurant, leading to a combinatorial explosion of methods. Instead, we can use the factory method pattern to create a separate factory for each restaurant, which will handle the creation of burgers specific to that restaurant.

# implmentation

# Product Interface

from abc import ABC, abstractmethod

class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass

class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# wheat variants : KingBurger menu

class BasicWheatBurger(Burger):
    def prepare(self):
        print("Preparing Basic Wheat Burger with bun, patty, and ketchup!")


class StandardWheatBurger(Burger):
    def prepare(self):
        print("Preparing Standard Wheat Burger with bun, patty, cheese, and lettuce!")


class PremiumWheatBurger(Burger):
    def prepare(self):
        print("Preparing Premium Wheat Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# Abstract Factory Interface

class BurgerFactory(ABC):
    @abstractmethod
    def create_burger(self, burger_type: str) -> Burger:
        pass

# Concrete Factory Classes

# Singh Burger Normal Buns 
class SinghBurger(BurgerFactory):
    def create_burger(self, burger_type: str) -> Burger:
        if burger_type == "basic":
            return BasicBurger()
        elif burger_type == "standard":
            return StandardBurger()
        elif burger_type == "premium":
            return PremiumBurger()
        else:
            raise ValueError("Invalid burger type")

# King Burger Wheat Buns

class SinghBurger(BurgerFactory):
    def create_burger(self, burger_type: str) -> Burger:
        if burger_type == "basic":
            return BasicBurger()
        elif burger_type == "standard":
            return StandardBurger()
        elif burger_type == "premium":
            return PremiumBurger()
        else:
            raise ValueError("Invalid burger type")


# client 

if __name__ == "__main__":

    burger_type = "basic"

    factory: BurgerFactory = SinghBurger()   # choose restaurant

    burger = factory.create_burger(burger_type)

    burger.prepare()


'''
observations with factory method pattern:
1. tommorow if I add a new resturant, i just have to create a new factory class for that restaurant, without modifying existing code.
2. But if i want to add a new burger type, I will have to modify all the existing factory classes to handle the new burger type. This is a limitation of the factory method pattern, as it does not fully adhere to the Open/Closed Principle when it comes to adding new product types.

'''