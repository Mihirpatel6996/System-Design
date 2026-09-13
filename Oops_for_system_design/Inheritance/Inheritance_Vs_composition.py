## Bad code 

class Engine:
    pass

class Car(Engine):   
    pass

## Good Code 

class Engine:
    pass

class Car:
    def __init__(self):
        self.engine = Engine()

# This is a better design because it uses composition instead of inheritance. The Car class has an Engine object as a member variable, which allows for better flexibility and encapsulation.
# Car is not a type of Engine, but rather it has an Engine. This is a more accurate representation of the relationship between the two classes.