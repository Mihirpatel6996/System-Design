'''
Whole Idea of Eager initialization :

Instead of creating the instance when it is requested for the first time, we create the instance at the time of class loading. This is called eager initialization. It is thread-safe without requiring special language constructs (i.e. volatile or synchronized). The drawback of this approach is that the instance is created even though the client application might not be using it making it resource intensive. This is a good approach if the singleton class is lightweight and the resource is not expensive to create.
'''

# Implementation

class Singleton:
    _instance = None  # will be assigned immediately after class definition

    def __init__(self):
        print("Constructor called")

    @classmethod
    def get_instance(cls):
        return cls._instance


# Eager initialization (happens at import / load time)
Singleton._instance = Singleton()


# Simulating main()
s1 = Singleton.get_instance()
s2 = Singleton.get_instance()

print("Are both objects same?", s1 is s2)


'''
when to use it 

1. object is lightweight and resource is not expensive to create.
2. object is used frequently in the application.
3. startup time of the application is not critical.



'''