# solution --> use abstraction -- one interface and multiple implementations
# Define Abstraction 

from abc import ABC, abstractmethod

class RetrievalStrategy(ABC):

    @abstractmethod
    def retrieve(self, query_embedding):
        pass

# Concrete Implementations

class LengthBasedRetriever(RetrievalStrategy):

    def retrieve(self, query_embedding):
        return "patient_length"

class KeywordRetriever(RetrievalStrategy):

    def retrieve(self, query_embedding):
        return "patient_keyword"

class CosineRetriever(RetrievalStrategy):

    def retrieve(self, query_embedding):
        return "patient_cosine"


# usage

class Retriever:

    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy

    def retrieve(self, query_embedding):
        return self.strategy.retrieve(query_embedding)

## Now we can add new retrieval strategies without modifying the existing Retriever class.

class BM25Retriever(RetrievalStrategy):

    def retrieve(self, query_embedding):
        return "patient_bm25"


