# instead of putting behaviors into robots we can create separate classes for each behavior and use composition to assign behaviors to robots. This way, we can easily change the behavior of a robot at runtime without modifying the robot class itself.

# Step 1 : Create strategy interfaces for each behavior

from abc import ABC, abstractmethod

# --- Walk Strategy --- --> strategy Interface 
class WalkBehavior(ABC):
    @abstractmethod
    def walk(self):
        pass

# --> Concrete Strategies
class NormalWalk(WalkBehavior): 
    def walk(self):
        print("Walking normally...")


class NoWalk(WalkBehavior):
    def walk(self):
        print("Cannot walk.")

# --- Talk Strategy ---
class TalkBehavior(ABC):
    @abstractmethod
    def talk(self):
        pass


class NormalTalk(TalkBehavior):
    def talk(self):
        print("Talking normally...")


class NoTalk(TalkBehavior):
    def talk(self):
        print("Cannot talk.")

# --- Fly Strategy ---
class FlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass


class NormalFly(FlyBehavior):
    def fly(self):
        print("Flying normally...")


class NoFly(FlyBehavior):
    def fly(self):
        print("Cannot fly.")

# Robot Base Class (Composition)

# Context 
class Robot(ABC):

    def __init__(self, walk_behavior, talk_behavior, fly_behavior):
        self.walk_behavior = walk_behavior
        self.talk_behavior = talk_behavior
        self.fly_behavior = fly_behavior

    def walk(self):
        self.walk_behavior.walk()

    def talk(self):
        self.talk_behavior.talk()

    def fly(self):
        self.fly_behavior.fly()

    @abstractmethod
    def projection(self):
        pass

# Concrete Robots

class CompanionRobot(Robot):
    def projection(self):
        print("Displaying friendly companion features...")

class WorkerRobot(Robot):
    def projection(self):
        print("Displaying worker efficiency stats...")


# System Design 


robot1 = CompanionRobot(
    NormalWalk(),
    NormalTalk(),
    NoFly()
)

robot1.walk()
robot1.talk()
robot1.fly()
robot1.projection()

print("--------------------")

robot2 = WorkerRobot(
    NoWalk(),
    NoTalk(),
    NormalFly()
)

robot2.walk()
robot2.talk()
robot2.fly()
robot2.projection()



