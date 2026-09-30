# we'll simulate this --> QueryEvent → [Retriever, Logger] → LLM → Response

# define the Observer interface

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# event manager class (subject)

class EventManager:

    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, observer: Observer):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(observer)

    def notify(self, event_type: str, data):
        if event_type in self._subscribers:
            for observer in self._subscribers[event_type]:
                observer.update(data)


# creating concrete observers

class Retriever(Observer):

    def update(self, query):
        print("[Retriever] Fetching documents for:", query)
        docs = ["doc1 about " + query, "doc2 about " + query]
        event_manager.notify("docs_retrieved", docs)

class QueryLogger(Observer):

    def update(self, query):
        print("[Logger] Logging query:", query)

class LLMProcessor(Observer):

    def update(self, docs):
        print("[LLM] Generating answer using docs:", docs)
        response = "Answer based on " + ", ".join(docs)
        # Tell system: "I’m done, next step can start"
        event_manager.notify("response_generated", response)

class ResponseLogger(Observer):

    def update(self, response):
        print("[ResponseLogger] Final Response:", response)

if __name__ == "__main__":

    event_manager = EventManager()

    # Register observers
    event_manager.subscribe("query_received", Retriever())
    event_manager.subscribe("query_received", QueryLogger())

    event_manager.subscribe("docs_retrieved", LLMProcessor())

    event_manager.subscribe("response_generated", ResponseLogger())

    # Trigger system
    user_query = "heart disease treatment"
    print("\n--- User Query Incoming ---\n")

    event_manager.notify("query_received", user_query)




"""
Output :

--- User Query Incoming ---

[Retriever] Fetching documents for: heart disease treatment
[LLM] Generating answer using docs: ['doc1 about heart disease treatment', 'doc2 about heart disease treatment']
[ResponseLogger] Final Response: Answer based on doc1 about heart disease treatment, doc2 about heart disease treatment
[Logger] Logging query: heart disease treatment
"""
