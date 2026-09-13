class Account:
    def __init__(self, balance):
        self.balance = balance
        self.transactions = []


acc = Account(1000)

acc.balance -= 5000          # invalid, goes negative
acc.transactions = []        # history wiped
acc.balance = "hello"        # type broken

'''
Problem:

No control over state
No place to enforce rules
Any part of code can corrupt it
'''