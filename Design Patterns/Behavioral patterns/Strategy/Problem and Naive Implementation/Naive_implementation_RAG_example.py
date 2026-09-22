'''
You are building a RAG pipeline:

User Query → Retrieve Documents → Generate Answer

But retrieval can vary:

Simple keyword search (BM25-like)
Vector search (embeddings)
Hybrid (keyword + vector)

'''

class RAGPipeline:

    def retrieve(self, query, retrieval_type):
        if retrieval_type == "keyword":
            return ["doc1_keyword", "doc2_keyword"]
        elif retrieval_type == "vector":
            return ["doc1_vector", "doc2_vector"]
        elif retrieval_type == "hybrid":
            return ["doc1_hybrid", "doc2_hybrid"]

    def generate(self, query, docs):
        return f"Answer based on {docs}"

'''
Problems
    Adding new retrieval = modifying class
    Violates Open/Closed
    Logic becomes messy at scale

'''