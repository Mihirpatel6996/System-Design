# compiletime polymorphism / method overloading
# Same method name, different parameter lists


'''
In Python, method overloading is not directly supported like in some other programming languages.
However, we can achieve a similar effect using default parameters or *args and **kwargs.
'''

# Approach -1: Using default parameters

class Calculator:
    def add(self, a, b, c=0):
        return a + b + c

calc = Calculator()

calc.add(2, 3)      # 5
calc.add(2, 3, 4)   # 9


# Approach -2 : Using *args (variable number of arguments/ flexible number of arguments)

class Calculator:
    def add(self, *args):
        return sum(args)

calc.add(2, 3)      # 5
calc.add(2, 3, 4)   # 9

class Printer:
    def print_data(self, data):
        if isinstance(data, str):
            print("String:", data)
        elif isinstance(data, int):
            print("Integer:", data)
