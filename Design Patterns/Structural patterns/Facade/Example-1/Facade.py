#Same sub-systems

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



# Facade layer

class ComputerFacade:
    def __init__(self):
        self.power = PowerSupply()
        self.cooling = CoolingSystem()
        self.cpu = CPU()
        self.memory = Memory()
        self.disk = HardDrive()
        self.bios = BIOS()
        self.os = OperatingSystem()

    def start_computer(self):
        print("----- Starting Computer (via Facade) -----")

        self.power.provide_power()
        self.cooling.start_fans()

        self.bios.boot(self.cpu, self.memory)

        self.disk.spin_up()
        self.os.load()

        print("Computer Booted Successfully!")

# Client with facade
class Client:
    def boot_system(self):
        computer = ComputerFacade()
        computer.start_computer()


client = Client()
client.boot_system()

