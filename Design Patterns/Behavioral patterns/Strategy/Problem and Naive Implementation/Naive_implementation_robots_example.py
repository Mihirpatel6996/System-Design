'''
Problem:

You are building a Robot system.

Each robot can:

walk
talk
fly

But not all robots behave the same way:

Some robots walk normally
Some cannot walk
Some can fly, some cannot
Some talk, some don’t
First instinct (what most people do)
'''

# “Robots have behaviors → I’ll just put all methods inside the class and override them.”

# Base Robot

from abc import ABC, abstractmethod

class Robot(ABC):

    @abstractmethod
    def walk(self):
        pass

    @abstractmethod
    def talk(self):
        pass

    @abstractmethod
    def fly(self):
        pass

    @abstractmethod
    def projection(self):
        pass

# Concrete Robots

# companion robot 
class CompanionRobot(Robot):

    def walk(self):
        print("Walking normally...")

    def talk(self):
        print("Talking normally...")

    def fly(self):
        print("Cannot fly.")

    def projection(self):
        print("Displaying friendly companion features...")

# worker robot
class WorkerRobot(Robot):

    def walk(self):
        print("Cannot walk.")

    def talk(self):
        print("Cannot talk.")

    def fly(self):
        print("Flying normally...")

    def projection(self):
        print("Displaying worker efficiency stats...")


robot1 = CompanionRobot()
robot1.walk()
robot1.talk()
robot1.fly()
robot1.projection()

print("-------------")

robot2 = WorkerRobot()
robot2.walk()
robot2.talk()
robot2.fly()
robot2.projection()


'''
observations:

1. Lots of code duplication -- walk, fly, talk -- logic repeated in each robot class
2. If we want to add a new robot type, we have to implement all methods again
3. If we add a new behavior (e.g., swim), we have to modify the base class and all subclasses - for Ex : for Companion + CrawlWalk + AIChat I may need to implement 3 new methods in the base class and all subclasses
4. If requirement changes - for Ex if every robot should use AI based talking instead of normal talking, we have to modify all subclasses - this violates OCP and also lots of manitainance issues
5. No runtime flexibility - we cannot change the behavior of a robot at runtime - for Ex if we want to change the talking behavior of a CompanionRobot from normal talking to AI based talking, we have to modify the class and recompile it. 
6. Robot class = identity + behavior ( Tightly coupled)
7. what we actually want is to have a robot with different behaviors that can be changed at runtime. We want to separate the identity of the robot from its behavior. This is where the Strategy pattern comes in.

Robot (identity)
   + WalkBehavior (pluggable)
   + TalkBehavior (pluggable)
   + FlyBehavior (pluggable)
   + SwimBehavior (pluggable)
'''



