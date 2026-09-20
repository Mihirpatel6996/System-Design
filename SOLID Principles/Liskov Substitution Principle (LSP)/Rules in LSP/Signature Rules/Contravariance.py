'''
Python doesn’t enforce strongly, but conceptually:

Input should be same or broader
'''

class Animal:
    pass


class Dog(Animal):
    pass

# bad design 

class Handler:
    def handle(self, animal: Animal):
        pass


class DogHandler(Handler):
    def handle(self, animal: Dog):  #  narrower input
        pass

# explanation : caller might pass an Animal, but DogHandler expects a Dog. This violates LSP because DogHandler cannot handle all Animals, only Dogs.
Handler().handle(Animal())

