class EmbeddingModel:
    def __init__(self):
        print("Loading embedding model...")
        self.model = self._load()

    def _load(self):
        return "heavy-embedding-model"

    def embed(self, text):
        return f"embedding({text})"


class VectorStore:
    def __init__(self):
        print("Connecting to vector DB...")
        self.connected = True

    def search(self, query_embedding):
        return ["doc1", "doc2"]


class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vstore = VectorStore()

    def query(self, text):
        emb = self.embedder.embed(text)
        docs = self.vstore.search(emb)
        return docs