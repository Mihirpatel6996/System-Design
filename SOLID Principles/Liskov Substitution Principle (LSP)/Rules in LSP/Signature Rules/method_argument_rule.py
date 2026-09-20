'''
Rule

Child should NOT make input requirements stricter
(i.e., should not narrow inputs)

'''

## Violation Example (Narrowing Input Types)

class Payment:
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def pay(self, amount: int):   # ❌ expects only int
        print("Processing card payment")

## why this is bad --> Parent allows any type of amount, but child restricts it to int only. This violates LSP.

## Correct Example (Accepting Same or Broader Input Types)

class Payment:
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def pay(self, amount):   # ✅ same contract
        print("Processing card payment")

'''
Input is controlled by the caller,child class must accept all inputs that the parent class accepts. If the child class narrows the input types, it can lead to unexpected behavior and break the substitutability of the child class for the parent class.
'''
