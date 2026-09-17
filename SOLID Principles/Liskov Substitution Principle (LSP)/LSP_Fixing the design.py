## we dont hack the child instead we fix the design of the parent class to accommodate the child class behavior using abstraction

## Split responsibilities of Account into two separate interfaces: one for accounts that allow withdrawals and another for accounts that do not allow withdrawals.

from abc import ABC, abstractmethod

class Account(ABC):

    @abstractmethod
    def deposit(self, amount):
        pass

class WithdrawableAccount(Account):

    @abstractmethod
    def withdraw(self, amount):
        pass

# now implement correctly

class SavingsAccount(WithdrawableAccount):

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

    # No withdraw → correct design

# Now system can process any account type without violating LSP.

def process(account: WithdrawableAccount):
    account.withdraw(100)

process(SavingsAccount(1000))  # works
process(FixedDepositAccount(1000))  #  compile-time/design-level prevention


'''
Remember this --> never narrow the behaviour of the parent class in the child class. I

In the violation example we have seen -- our parent class Account allowed withdraw but our child class FixedDepositAccount did not allow withdraw. so the child class is narrowing the behaviour of the parent class which is a violation of LSP.



'''
