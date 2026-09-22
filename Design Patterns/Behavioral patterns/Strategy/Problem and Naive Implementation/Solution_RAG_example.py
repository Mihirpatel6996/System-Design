# Strategy Interface 
from abc import ABC, abstractmethod

# --- STRATEGY INTERFACE ---
class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve(self, query: str):
        pass


# Concrete Strategies 

# --- CONCRETE STRATEGY 1 ---
class KeywordRetrieval(RetrievalStrategy):
    def retrieve(self, query: str):
        print("[KeywordRetrieval] Searching using keywords...")
        return ["keyword_doc1", "keyword_doc2"]


# --- CONCRETE STRATEGY 2 ---
class VectorRetrieval(RetrievalStrategy):
    def retrieve(self, query: str):
        print("[VectorRetrieval] Searching using embeddings...")
        return ["vector_doc1", "vector_doc2"]


# --- CONCRETE STRATEGY 3 ---
class HybridRetrieval(RetrievalStrategy):
    def retrieve(self, query: str):
        print("[HybridRetrieval] Combining keyword + vector...")
        return ["hybrid_doc1", "hybrid_doc2"]

# Context RAG Pipeline

# --- CONTEXT --- --> Holds a reference to a strategy object, and delegates the retrieval to it
class RAGPipeline:

    def __init__(self, retrieval_strategy: RetrievalStrategy):
        self.retrieval_strategy = retrieval_strategy

    def set_strategy(self, retrieval_strategy: RetrievalStrategy):
        # runtime change possible
        self.retrieval_strategy = retrieval_strategy

    def run(self, query: str):
        # Delegation happens here
        docs = self.retrieval_strategy.retrieve(query)

        # generation step (simplified)
        answer = self.generate(query, docs)
        return answer

    def generate(self, query, docs):
        return f"Answer for '{query}' using {docs}"

# client code

# chose Strategy at runtime

Strategy = KeywordRetrieval
rag  = RAGPipeline(retrieval_strategy=Strategy)
rag.run("What is the capital of France?")

print("-------------Switchng Strategy at runtime-------------")


strategy = VectorRetrieval
rag.set_strategy(strategy)
rag.run("What is the capital of France?")






