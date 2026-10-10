class PowerSupply:
    def provide_power(self):
        print("Power Supply: Providing power...")


class CoolingSystem:
    def start_fans(self):
        print("Cooling System: Fans started...")


class CPU:
    def initialize(self):
        print("CPU: Initialization started...")


class Memory:
    def self_test(self):
        print("Memory: Self-test passed...")


class HardDrive:
    def spin_up(self):
        print("Hard Drive: Spinning up...")


class BIOS:
    def boot(self, cpu, memory):
        print("BIOS: Booting CPU and Memory checks...")
        cpu.initialize()
        memory.self_test()


class OperatingSystem:
    def load(self):
        print("Operating System: Loading into memory...")


# Client without facade

class Client:
    def start_computer(self):
        power = PowerSupply()
        cooling = CoolingSystem()
        cpu = CPU()
        memory = Memory()
        disk = HardDrive()
        bios = BIOS()
        os = OperatingSystem()

        print("----- Starting Computer -----")

        power.provide_power()
        cooling.start_fans()
        bios.boot(cpu, memory)
        disk.spin_up()
        os.load()

        print("Computer Booted Successfully!")

if __name__ == "__main__":
    client = Client()
    client.start_computer()

