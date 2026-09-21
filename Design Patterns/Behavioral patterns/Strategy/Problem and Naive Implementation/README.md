1. Problem Statement (Why Strategy Pattern exists)

Let’s forget your code for a moment and think like an engineer building a system.

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

You model robots using inheritance:

Robot
 ├── CompanionRobot
 ├── WorkerRobot
 ├── FlyingRobot
 ├── SilentRobot
 ├── NoWalkRobot
 ├── ...

Now answer this carefully:

What happens if you combine behaviors?

Example:

Robot that walks + talks + flies
Robot that walks + doesn’t talk + doesn’t fly
Robot that doesn’t walk + talks + flies

You get combinatorial explosion.

WalkTalkFlyRobot
WalkNoTalkFlyRobot
NoWalkTalkFlyRobot
NoWalkNoTalkFlyRobot