1. What is Command Pattern (core idea)
Forget the textbook definition for a moment.
Real-world intuition
Think of a restaurant:
- You (client) don’t directly go to kitchen (receiver)
- You don’t cook food yourself
- You also don’t care how chef cooks
Instead:
- You write an order slip
- Waiter takes it
- Chef executes it
That order slip = Command
Key idea:
Command pattern converts a request into an object.

That object:
- stores what needs to be done
- can be passed around
- can be executed later
- can be undone (optional)
Why this exists (the real problem)
Without Command pattern:
- Button directly calls light.on()
- Another button calls fan.on()
Now UI (button) is tightly coupled to devices.
If tomorrow:
- you add AC
- change fan logic
- add scheduling
- add undo
You start modifying button logic again and again.
That becomes a scaling nightmare.
Command pattern solves this:
It introduces a middle layer:
Button → Command Object → Device (Receiver)

So button doesn’t know:
- light
- fan
- AC
- kitchen oven
It only knows:
- “I execute a command”
The mental model shift
Without Command:
“Button calls device method directly”

With Command:
“Button triggers an object that knows what to do”

What Command really is
A Command object contains:
1. Receiver (actual device)
2. Action (what to do: on/off/etc)
3. execute()
4. (optional) undo()
In your system design language
Command pattern gives you:
- Decoupling of invoker and receiver
- Pluggable behavior at runtime
- Action as first-class object
Before code (important insight)
Ask yourself:
Why not just call light.on() directly?

Because then:
- UI and business logic are coupled
- no undo
- no queueing
- no logging
- no retries
- no scheduling
- no macros
Command pattern exists because real systems need:
- retry queues (payment systems)
- job scheduling (cron systems)
- undo/redo (editor apps)
- remote execution (home automation / IoT)
Now we move to next step
Next we’ll do:
Step 2: Naive implementation (NO command pattern)
We will intentionally break design:
- RemoteController directly calls Light/Fan
Then we’ll see:
- where it fails
- why it becomes unscalable

2. Naive Implementation (NO Command Pattern)
Problem setup (home automation)
We have:
- Light
- Fan
- Remote Controller (buttons)
We want:
- button 0 → light ON/OFF
- button 1 → fan ON/OFF
Naive idea (direct coupling)
We skip Command objects completely.
Code (bad design intentionally)
class Light:    def on(self):        print("Light is ON")    def off(self):        print("Light is OFF")class Fan:    def on(self):        print("Fan is ON")    def off(self):        print("Fan is OFF")


Remote controller directly controlling devices
class RemoteController:    def __init__(self):        self.light = None        self.fan = None        self.state = {}  # track ON/OFF state per button    def set_light(self, light):        self.light = light        self.state["light"] = False  # OFF initially    def set_fan(self, fan):        self.fan = fan        self.state["fan"] = False    def press_light_button(self):        if not self.state["light"]:            self.light.on()        else:            self.light.off()        self.state["light"] = not self.state["light"]    def press_fan_button(self):        if not self.state["fan"]:            self.fan.on()        else:            self.fan.off()        self.state["fan"] = not self.state["fan"]


Main usage
light = Light()fan = Fan()remote = RemoteController()remote.set_light(light)remote.set_fan(fan)remote.press_light_button()  # ONremote.press_light_button()  # OFFremote.press_fan_button()    # ONremote.press_fan_button()    # OFF


3. What is WRONG here (this is the real learning)
Now think like a system designer.
Problem 1: Remote is tightly coupled to devices
Remote knows:
- light
- fan
What if tomorrow you add:
- AC
- TV
- Heater
- Music system
You must modify:
RemoteController


👉 This violates Open/Closed Principle
Problem 2: Logic duplication
Every device needs:
- ON logic
- OFF logic
- state tracking
Remote is doing:
- toggle logic
- state management
So now remote is not a remote anymore → it's a device manager
Problem 3: No extensibility (BIG SYSTEM ISSUE)
Imagine scaling to:
- 100 devices
- 1000 buttons (smart home panel)
Now RemoteController becomes:
- huge if-else / method explosion
- impossible to maintain
Problem 4: No abstraction of “action”
Right now:
pressing button = directly calling method

But in real systems:
A button press might mean:
- turn on light
- dim light
- schedule light
- log action
- retry on failure
You cannot plug logic dynamically.
Problem 5: No undo / replay / queue
You cannot:
- store actions
- retry actions
- undo actions
- schedule actions
Because actions are not objects.
4. What we learned (critical insight)
This naive design says:
“Invoker directly controls receiver”

That works only when system is tiny.
But real systems need:
“Invoker should not know receiver at all”

5. Transition insight (this is the key)
We need to change thinking from:
❌ Bad:
“Button calls light.on()”
✅ Good:
“Button triggers a command”
So we introduce:
Button → Command → Device

Now Button is blind to:
- device type
- operation details
Next Step
Now we fix this using Command Pattern properly in Python.
We will build:
- Command interface
- LightCommand
- FanCommand
- RemoteController (generic, reusable)
Then I’ll show you:
- how undo becomes trivial
- how scaling becomes easy

3. Command Pattern (Proper Design in Python)
Core idea we are introducing
We are separating:
- Invoker → Remote (just triggers)
- Command → “what to do”
- Receiver → Light / Fan (actual device)
So now:
Remote (Invoker) → Command → Device (Receiver)

Remote does NOT know Light or Fan anymore.
Step 1: Command abstraction
In Python, we don’t have interfaces like Java, so we use a base class.
from abc import ABC, abstractmethod


Command interface
class Command(ABC):    @abstractmethod    def execute(self):        pass    @abstractmethod    def undo(self):        pass


Why this exists
We are standardizing:
Every action must support:

- do (execute)
- revert (undo)
This is what makes commands powerful in real systems:
- retry systems
- job queues
- transactional systems
Step 2: Receivers (real devices)
These are unchanged business objects.
class Light:    def on(self):        print("Light is ON")    def off(self):        print("Light is OFF")


class Fan:    def on(self):        print("Fan is ON")    def off(self):        print("Fan is OFF")


Step 3: Concrete Commands
Now we wrap device actions inside objects.
Light Command
class LightCommand(Command):    def __init__(self, light: Light):        self.light = light        self.is_on = False    def execute(self):        self.light.on()        self.is_on = True    def undo(self):        if self.is_on:            self.light.off()            self.is_on = False


Fan Command
class FanCommand(Command):    def __init__(self, fan: Fan):        self.fan = fan        self.is_on = False    def execute(self):        self.fan.on()        self.is_on = True    def undo(self):        if self.is_on:            self.fan.off()            self.is_on = False


Step 4: Invoker (Remote Controller)
Now THIS is the key transformation.
Remote becomes:
- generic
- device-agnostic
- reusable
class RemoteController:    def __init__(self, size=4):        self.buttons = [None] * size        self.state = [False] * size  # ON/OFF tracking    def set_command(self, idx, command: Command):        self.buttons[idx] = command        self.state[idx] = False    def press_button(self, idx):        if not self.buttons[idx]:            print(f"No command assigned to button {idx}")            return        if not self.state[idx]:            self.buttons[idx].execute()        else:            self.buttons[idx].undo()        self.state[idx] = not self.state[idx]


Step 5: Client code (usage)
light = Light()fan = Fan()light_cmd = LightCommand(light)fan_cmd = FanCommand(fan)remote = RemoteController()remote.set_command(0, light_cmd)remote.set_command(1, fan_cmd)print("--- Light ---")remote.press_button(0)  # ONremote.press_button(0)  # OFFprint("--- Fan ---")remote.press_button(1)  # ONremote.press_button(1)  # OFF


4. What changed (this is the real understanding)
Before (bad design)
Remote → Light/Fan directly

Problems:
- tight coupling
- no extensibility
- no undo abstraction
After (Command pattern)
Remote → Command → Device

Now:
Remote only knows:
- "I execute something"
Command knows:
- what to do
- how to undo it
Device knows:
- only business logic
5. Why Command pattern is powerful (real systems view)
This is not just about buttons.
This pattern is used in:
1. Task queues (Celery / Kafka consumers)
Instead of:
- calling function directly
You do:
- serialize command
- queue it
- execute later
2. Undo/Redo (editors like Photoshop, VS Code)
Every action is a command:
- draw line
- erase
- move object
Undo = reverse command stack
3. Retry systems (payments / APIs)
If execution fails:
- re-run same command object
4. Scheduling systems (cron jobs)
Store commands and execute later.
6. Key mental model (MOST IMPORTANT)
Think of Command as:
“A packaged action that can travel through a system”

Not:
“A function call wrapper”