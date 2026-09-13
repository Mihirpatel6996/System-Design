'''
Final Implementation of Polymorphism in Python

Practice (important)

Implement:

Base
Shape
    area()
Children
Circle
Rectangle

Then:

def compute_area(shape):
    return shape.area()
'''

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

def compute_area(shape: Shape):
    return shape.area()


shape1 = Circle(5)
shape2 = Rectangle(4, 6)
print(f"Area of Circle: {compute_area(shape1)}")
print(f"Area of Rectangle: {compute_area(shape2)}")



