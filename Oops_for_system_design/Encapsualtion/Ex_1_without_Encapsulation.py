class BankAccount:
    def __init__(self, balance):
        self.balance = balance   # public

account = BankAccount(1000)

# Anywhere in code:
account.balance = -999999   # No control