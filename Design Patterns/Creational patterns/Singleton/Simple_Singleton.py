class Singleton:
    _instance = None  # class-level variable (shared across all calls)

    def __init__(self):
        print("Constructor called")

    @classmethod
    def get_instance(cls): # why cls here : Because we are using class method, so we need to use cls to refer to the class itself
        if cls._instance is None:
            cls._instance = cls()   # create only once
        return cls._instance


# Simulating main()
s1 = Singleton.get_instance()
s2 = Singleton.get_instance()

print("Are both objects same?", s1 is s2)

'''
Output :
Constructor called
Are both objects same? True

'''

'''
Problem with simple singleton is that it is not thread safe. If multiple threads are trying to access the get_instance method at the same time, it can lead to multiple instances being created. To make it thread safe, we can use a lock to ensure that only one thread can create the instance at a time.

For Ex t1 and t2 are two threads trying to access the get_instance method at the same time. If t1 checks if _instance is None and finds it to be True, it will proceed to create a new instance. Meanwhile, t2 also checks if _instance is None and finds it to be True as well, since t1 has not yet created the instance. As a result, both threads will create separate instances of the Singleton class, violating the singleton pattern.
'''

# solution --> Thread safe singleton