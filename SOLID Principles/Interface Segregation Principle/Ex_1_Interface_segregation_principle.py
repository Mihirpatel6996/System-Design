# Definition : Clients should not be forced to depend on interfaces they don't use.

## problem : lets say we are defining a single interface for data systems
class DataService:
    def store(self, data):
        pass

    def retrieve(self, query):
        pass

    def stream(self):
        pass

    def delete(self, id):
        pass

# looks clean right - but lets implement in different systems

class SQLService(DataService):

    def store(self, data):
        print("store in DB")

    def retrieve(self, query):
        print("query DB")

    def stream(self):
        raise NotImplementedError()   # Not applicable for SQL

    def delete(self, id):
        print("delete row")

class KafkaService(DataService):

    def store(self, data):
        print("produce message")

    def retrieve(self, query):
        raise NotImplementedError()   # Not applicable for Kafka

    def stream(self):
        print("consume stream")

    def delete(self, id):
        raise NotImplementedError()   # Not applicable for Kafka


'''
Where It Breaks

You now have:
    Methods that exist but are meaningless for that class

This leads to:
    Runtime errors (NotImplementedError)
    Confusing APIs
    Tight coupling
    Fake implementations

'''
# fix : break the interface into smaller, more specific interfaces

from abc import ABC, abstractmethod

class Storable(ABC):
    @abstractmethod
    def store(self, data):
        pass


class Retrievable(ABC):
    @abstractmethod
    def retrieve(self, query):
        pass


class Streamable(ABC):
    @abstractmethod
    def stream(self):
        pass


class Deletable(ABC):
    @abstractmethod
    def delete(self, id):
        pass

# Implement only what's needed 

# SQL service implements Storable, Retrievable, Deletable

class SQLService(Storable, Retrievable, Deletable):

    def store(self, data):
        print("store in DB")

    def retrieve(self, query):
        print("query DB")

    def delete(self, id):
        print("delete row")

# Kafka service implements Storable, Streamable

class KafkaService(Storable, Streamable):

    def store(self, data):
        print("produce message")

    def stream(self):
        print("consume stream")


'''
What Changed (Important Insight)

Now:
    No fake methods
    No NotImplementedError
    Each class has only relevant responsibilities
'''

    