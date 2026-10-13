# Same subsystems for RAG
class EmbeddingModel:
    def embed(self, text):
        print(f"Embedding text: {text}")
        return f"embedding({text})"


class VectorDB:
    def search(self, embedding):
        print(f"Searching for embedding: {embedding}")
        return ["doc1", "doc2", "doc3"]


class Reranker:
    def rerank(self, query, docs):
        print(f"Reranking docs: {docs} for query: {query}")
        return sorted(docs)[:2]


class LLM:
    def generate(self, query, context):
        print(f"Generating answer for query: {query} with context: {context}")
        return f"Answer based on {context} for {query}"


class PostProcessor:
    def clean(self, text):
        print(f"Cleaning text: {text}")
        return text.strip()


# facade class to simplify the interaction with the subsystems

class RAGFacade:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vectordb = VectorDB()
        self.reranker = Reranker()
        self.llm = LLM()
        self.post = PostProcessor()

    def query(self, user_query):
        print("RAG Pipeline started")

        # Step 1: embedding
        embedding = self.embedder.embed(user_query)

        # Step 2: retrieval
        docs = self.vectordb.search(embedding)

        # Step 3: reranking
        top_docs = self.reranker.rerank(user_query, docs)

        # Step 4: generation
        response = self.llm.generate(user_query, top_docs)

        # Step 5: post processing
        final_response = self.post.clean(response)

        return final_response


class Client:
    def __init__(self):
        self.rag = RAGFacade()

    def ask(self, query):
        return self.rag.query(query)


client = Client()

if __name__ == "__main__":
    answer = client.ask("What is RAG?")
    print(answer)



