class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

acc = Account(1000)
print(acc.balance)  # you will get 1000
acc.balance = 4000
print(acc.balance)  # you will get 4000
acc.balance = -1000  # this will raise a ValueError

'''
This gives:

clean syntax
controlled access
flexibility to change logic later

'''