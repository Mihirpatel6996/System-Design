import time

# Heavy objects that we want to delay loading until necessary

class RealEmbeddingModel:
    def __init__(self):
        print("Loading embedding model from disk...")
        time.sleep(2)

    def embed(self, text):
        return f"embedding({text})"


class RealVectorStore:
    def __init__(self):
        print("Connecting to Vector DB...")
        time.sleep(2)

    def search(self, query_embedding):
        return ["doc1", "doc2"]


# Virtual Proxy Layer

class EmbeddingProxy:
    def __init__(self):
        self._real = None

    def embed(self, text):
        if self._real is None:
            print("[Proxy] Lazy loading embedding model...")
            self._real = RealEmbeddingModel()
        return self._real.embed(text)


class VectorStoreProxy:
    def __init__(self):
        self._real = None

    def search(self, emb):
        if self._real is None:
            print("[Proxy] Lazy connecting to Vector DB...")
            self._real = RealVectorStore()
        return self._real.search(emb)


# RAG Pipeline that uses proxies

class RAGPipeline:
    def __init__(self):
        print("Initializing RAG pipeline (lightweight)...")
        self.embedder = EmbeddingProxy()
        self.vstore = VectorStoreProxy()

    def query(self, text):
        print("\nUser query received:", text)

        emb = self.embedder.embed(text)
        docs = self.vstore.search(emb)

        return docs

if __name__ == "__main__":
    rag = RAGPipeline()

    print("\n--- System ready ---\n")

    print(rag.query("what is RAG?"))