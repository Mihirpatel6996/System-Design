# lets model accounts in a bank

class Account:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount


class SavingsAccount(Account):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

class FixedDepositAccount(Account):

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        raise Exception("Cannot withdraw before maturity")  # ❌


# where it breaks 

# now system expects to process any account type, but FixedDepositAccount violates LSP because it cannot be used in place of Account without breaking the system.
def process(account: Account):
    account.withdraw(100)

# works
process(SavingsAccount(1000))

# breaks 
process(FixedDepositAccount(1000))  # ❌ raises Exception


# why this violats LSP:

# Base class says withdraw is allowed, but FixedDepositAccount does not allow it. This means that FixedDepositAccount cannot be used in place of Account without breaking the system, which violates the Liskov Substitution Principle.

# so child is not sustituable for parent 

# LSP is about behavioural contracts. not just method names 

'''
 
Contract of Account

Implicitly:

deposit should work
withdraw should work

But FixedDepositAccount breaks this contract.


'''

# Solution --> LSP_Fixing the design.py


