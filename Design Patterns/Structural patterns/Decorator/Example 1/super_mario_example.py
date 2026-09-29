# Step 1 : Basic Interface + mario class
# 
# from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

# 1. Component Interface
class Character(ABC):

    @abstractmethod
    def get_abilities(self) -> str:
        pass


# 2. Concrete Component
class Mario(Character):

    def get_abilities(self) -> str:
        return "Mario" 


# Step -2 Decorator Base Class

# 3. Abstract Decorator
class CharacterDecorator(Character):

    def __init__(self, character: Character):
        self.character = character

    def get_abilities(self) -> str:
        return self.character.get_abilities()


"""
We just created is-a and has-a relationship between the decorator and the component. CharacterDecorator is-a Character and has-a Character. This is the key to the decorator pattern. The decorator class implements the same interface as the component it decorates, allowing it to be used interchangeably with the component. Additionally, it holds a reference to a Character object, enabling it to delegate calls to the wrapped object while adding its own behavior.
"""

# Concrete decorators 

# 1. height power up 

class HeightUp(CharacterDecorator):

    def __init__(self, character: Character):
        super().__init__(character)

    def get_abilities(self) -> str:
        return self.character.get_abilities() + " + HeightUp"

# 2. Gun power up

class GunPowerUp(CharacterDecorator):

    def __init__(self, character: Character):
        super().__init__(character)

    def get_abilities(self) -> str:
        return self.character.get_abilities() + " + Gun"

# 3. star power up

class StarPowerUp(CharacterDecorator):

    def __init__(self, character: Character):
        super().__init__(character)

    def get_abilities(self) -> str:
        return self.character.get_abilities() + " + Star Power (Limited)"


#Client Code

if __name__ == "__main__":

    mario = Mario()
    print(mario.get_abilities())
    # Mario

    height_up_mario = HeightUp(mario)
    print(height_up_mario.get_abilities())
    # Mario + HeightUp

    height_up_gun_power_mario = GunPowerUp(height_up_mario)
    print(height_up_gun_power_mario.get_abilities())
    # Mario + HeightUp + Gun

    height_up_gun_power_star_power_mario = StarPowerUp(height_up_gun_power_mario)
    print(height_up_gun_power_star_power_mario.get_abilities())
    # Mario + HeightUp + Gun + Star Power (Limited)


    mario = StarPowerUp(
            GunPowerUp(
                HeightUp(
                    Mario()
                )
            )
        )

print(mario.get_abilities())