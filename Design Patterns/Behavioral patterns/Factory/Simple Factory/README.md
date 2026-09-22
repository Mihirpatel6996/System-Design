A Simple Factory is a centralized piece of code that decides which object to create based on input.

Instead of the client doing:

if type == "basic":
    burger = BasicBurger()
elif type == "standard":
    burger = StandardBurger()

You move that decision into one place:

Client → Factory → Concrete Object

Why this matters (think like a system designer)

Right now your system is small. But imagine:

20 burger types
Multiple teams adding new burgers
Same creation logic used across APIs, workers, tests

If every place has if/else, your system becomes unmaintainable quickly.

So we centralize object creation.

Core Idea
Client does NOT know which class to instantiate
Factory knows all concrete classes
Client only asks: "give me X"

