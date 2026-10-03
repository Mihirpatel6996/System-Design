"""
Problem setup (home automation)
    We have:
    - Light
    - Fan
- Remote Controller (buttons)
    We want:
    - button 0 → light ON/OFF
    - button 1 → fan ON/OFF

"""

# Naive Idea would be to directly implement the button functionality in the RemoteController class. 

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



# RemoteController directly controls the Light and Fan. 

class RemoteController:
    def __init__(self):
        self.light = None
        self.fan = None
        self.state = {}  # track ON/OFF state per button

    def set_light(self, light: Light) -> None: 
        self.light = light
        self.state["light"] = False  # OFF initially

    def set_fan(self, fan: Fan) ->None :
        self.fan = fan
        self.state["fan"] = False

    def press_light_button(self):
        if not self.state["light"]:
            self.light.on()
        else:
            self.light.off()
        self.state["light"] = not self.state["light"]

    def press_fan_button(self):
        if not self.state["fan"]:
            self.fan.on()
        else:
            self.fan.off()
        self.state["fan"] = not self.state["fan"]


light = Light()
fan = Fan()

remote = RemoteController()
remote.set_light(light)
remote.set_fan(fan)

remote.press_light_button()  # ON
remote.press_light_button()  # OFF

remote.press_fan_button()    # ON
remote.press_fan_button()    # OFF


"""
Problems with this naive implementation:
1. RemoteController class is tightly coupled with Light and Fan classes. If we want to add more devices, we need to modify the RemoteController class.
2. RemoteController class has to know the details of how to turn on/off each device. If we want to change the implementation of Light or Fan, we need to modify the RemoteController class.
3. RemoteController class has to maintain the state of each device. If we want to add more devices, we need to modify the RemoteController class.
4. Every device needs On/Off logic and state menagement. so RemoteController is not remote anymore its a device manager.
5. Cannot scale to more devices easily. If we want to add more devices, we need to modify the RemoteController class.
6. no undo/redo functionality. Retry and schedule actions are not possible. We need to modify the RemoteController class.
"""

