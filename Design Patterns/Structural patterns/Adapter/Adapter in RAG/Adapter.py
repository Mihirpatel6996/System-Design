# Adapter interface for the Retriever class

class Retriever:
    def get_documents(self, query: str) -> list[str]:
        raise NotImplementedError

# Adaptee classes (existing classes that we cannot modify)

class VectorDB:
    def search(self, query):
        return [
            {"page_content": "vector doc 1"},
            {"page_content": "vector doc 2"}
        ]


class APIClient:
    def fetch(self, query):
        return {
            "results": ["api doc 1", "api doc 2"]
        }

# Adapters 

class VectorDBAdapter(Retriever):
    def __init__(self, vectordb: VectorDB):
        self.vectordb = vectordb

    def get_documents(self, query: str) -> list[str]:
        results = self.vectordb.search(query)
        return [doc["page_content"] for doc in results]


class APIAdapter(Retriever):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_documents(self, query: str) -> list[str]:
        response = self.api_client.fetch(query)
        return response["results"]


class RAGPipeline:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def run(self, query: str):
        docs = self.retriever.get_documents(query)
        return self.generate_answer(docs)

    def generate_answer(self, docs):
        return f"LLM answer using: {docs}"
# Usuage

if __name__ == "__main__":
    vectordb = VectorDB()
    retriever = VectorDBAdapter(vectordb)

    pipeline = RAGPipeline(retriever)
    print(pipeline.run("What is AI?"))



