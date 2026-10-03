# Command -> Invoker, command, receiver

# remote --> command -> devices

# Command Interface

from abc import ABC, abstractmethod

class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Devices 

class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")

class Fan:
    def on(self):
        print("Fan is ON")

    def off(self):
        print("Fan is OFF")

# Concrete commands

class LightCommand(Command):

    def __init__(self, light: Light):
        self.light = light
        self.is_on = False

    def execute(self):
        self.light.on()
        self.is_on = True

    def undo(self):
        if self.is_on:
            self.light.off()
            self.is_on = False

class FanCommand(Command):

    def __init__(self, fan: Fan):
        self.fan = fan
        self.is_on = False

    def execute(self):
        self.fan.on()
        self.is_on = True

    def undo(self):
        if self.is_on:
            self.fan.off()
            self.is_on = False


# Invoker --> 
class RemoteController:

    def __init__(self, size=4):
        self.buttons = [None] * size
        self.state = [False] * size  # ON/OFF tracking

    def set_command(self, idx, command: Command):
        self.buttons[idx] = command
        self.state[idx] = False

    def press_button(self, idx):
        if not self.buttons[idx]:
            print(f"No command assigned to button {idx}")
            return

        if not self.state[idx]:
            self.buttons[idx].execute()
        else:
            self.buttons[idx].undo()

        self.state[idx] = not self.state[idx]


# Client code

light = Light()
fan = Fan()

light_cmd = LightCommand(light)
fan_cmd = FanCommand(fan)

remote = RemoteController()

remote.set_command(0, light_cmd)
remote.set_command(1, fan_cmd)

print("--- Light ---")
remote.press_button(0)  # ON
remote.press_button(0)  # OFF

print("--- Fan ---")
remote.press_button(1)  # ON
remote.press_button(1)  # OFF




