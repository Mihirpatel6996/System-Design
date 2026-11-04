# Base handler 

class MoneyHandler:
    def __init__(self):
        self.next_handler: 'MoneyHandler' = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler  # enables chaining

    def dispense(self, amount):
        raise NotImplementedError


# Concrete handlers

class ThousandHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 1000

        if notes_needed > self.num_notes:
            notes_to_use = self.num_notes
            self.num_notes = 0
        else:
            notes_to_use = notes_needed
            self.num_notes -= notes_to_use

        if notes_to_use > 0:
            print(f"Dispensing {notes_to_use} x ₹1000 notes")

        remaining = amount - (notes_to_use * 1000)

        if remaining > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining)
            else:
                print(f"Remaining ₹{remaining} cannot be dispensed")



# Concrete handlers

class FiveHundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 500

        if notes_needed > self.num_notes:
            notes_to_use = self.num_notes
            self.num_notes = 0
        else:
            notes_to_use = notes_needed
            self.num_notes -= notes_to_use

        if notes_to_use > 0:
            print(f"Dispensing {notes_to_use} x ₹500 notes")

        remaining = amount - (notes_to_use * 500)

        if remaining > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining)
            else:
                print(f"Remaining ₹{remaining} cannot be dispensed")



class TwoHundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 200

        if notes_needed > self.num_notes:
            notes_to_use = self.num_notes
            self.num_notes = 0
        else:
            notes_to_use = notes_needed
            self.num_notes -= notes_to_use

        if notes_to_use > 0:
            print(f"Dispensing {notes_to_use} x ₹200 notes")

        remaining = amount - (notes_to_use * 200)

        if remaining > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining)
            else:
                print(f"Remaining ₹{remaining} cannot be dispensed")



class HundredHandler(MoneyHandler):
    def __init__(self, num_notes):
        super().__init__()
        self.num_notes = num_notes

    def dispense(self, amount):
        notes_needed = amount // 100

        if notes_needed > self.num_notes:
            notes_to_use = self.num_notes
            self.num_notes = 0
        else:
            notes_to_use = notes_needed
            self.num_notes -= notes_to_use

        if notes_to_use > 0:
            print(f"Dispensing {notes_to_use} x ₹100 notes")

        remaining = amount - (notes_to_use * 100)

        if remaining > 0:
            if self.next_handler:
                self.next_handler.dispense(remaining)
            else:
                print(f"Remaining ₹{remaining} cannot be dispensed")


# Create handlers
h1000 = ThousandHandler(3)
h500 = FiveHundredHandler(5)
h200 = TwoHundredHandler(10)
h100 = HundredHandler(20)

# Build chain
h1000.set_next(h500).set_next(h200).set_next(h100)


amount = 3700
print(f"\nDispensing ₹{amount}")
h1000.dispense(amount)


"""
1000 handler:
  uses 3 notes → ₹3000
  remaining = ₹700 → pass

500 handler:
  uses 1 note → ₹500
  remaining = ₹200 → pass

200 handler:
  uses 1 note → ₹200
  remaining = ₹0 → stop

"""