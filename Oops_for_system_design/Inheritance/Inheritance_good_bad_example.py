# Good Example 

class Cache:
    def get(self, key): pass

class RedisCache(Cache):
    def get(self, key): pass

class MemoryCache(Cache):
    def get(self, key): pass



# Bad Example

class Bird:
    def fly(self): pass

class Penguin(Bird):
    def fly(self): raise Exception("Cannot fly")  # This is a bad example because penguins are birds but they cannot fly. So, if we have a method that expects a Bird object and calls the fly method, it will break for penguins. This violates the Liskov Substitution Principle (LSP) which states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.

