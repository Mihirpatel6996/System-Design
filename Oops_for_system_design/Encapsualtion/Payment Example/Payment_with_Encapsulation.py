class Account:
    def __init__(self, balance):
        self.__balance = balance
        self.__transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        self.__balance += amount
        self.__transactions.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        if amount > self.__balance:
            raise ValueError("Insufficient balance")

        self.__balance -= amount
        self.__transactions.append(("withdraw", amount))

    def get_balance(self):
        return self.__balance

    def get_transactions(self):
        return list(self.__transactions)  # return copy


'''
Key points:

State is not directly writable
All updates go through controlled logic
Invariants are enforced (no negative balance)
Internal structure is protected

'''

Mihir = Account(1000)
print(Mihir.get_balance()) # you will get 1000
Mihir.balance = 4000
print(Mihir.get_balance()) # still you will get 1000, because balance is private and cannot be modified directly
Mihir.balance -= 1000
print(Mihir.get_balance()) # still you will get 1000, because balance is private and cannot be modified directly
Mihir._Account__balance -= 1000
print(Mihir.get_balance()) # now you will get 0, because we are accessing the private variable directly using name mangling, but this is not recommended






