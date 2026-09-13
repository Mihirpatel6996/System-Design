class BankAccount:
    def __init__(self, balance):
        self.__balance = balance   # private can be defined with double underscore 

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount

    def get_balance(self):
        return self.__balance