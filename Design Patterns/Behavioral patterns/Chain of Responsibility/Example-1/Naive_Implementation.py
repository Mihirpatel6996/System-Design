class ATM:
    def __init__(self):
        self.notes = {
            1000: 3,
            500: 5,
            200: 10,
            100: 20
        }

    def dispense(self, amount):
        print(f"\nDispensing amount: ₹{amount}")

        for denom in [1000, 500, 200, 100]:
            if amount <= 0:
                break

            available = self.notes[denom]
            needed = amount // denom

            used = min(needed, available)

            if used > 0:
                print(f"Dispensing {used} x ₹{denom}")
                self.notes[denom] -= used
                amount -= used * denom

        if amount > 0:
            print(f"Remaining ₹{amount} cannot be dispensed")

atm = ATM()
atm.dispense(3700)