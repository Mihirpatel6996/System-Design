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



# Client Bad Design 

class Client:
    def ask(self, query):
        embedder = EmbeddingModel()
        vectordb = VectorDB()
        reranker = Reranker()
        llm = LLM()
        post = PostProcessor()

        embedding = embedder.embed(query)
        docs = vectordb.search(embedding)
        top_docs = reranker.rerank(query, docs)

        response = llm.generate(query, top_docs)
        final = post.clean(response)

        return final


if __name__ == "__main__":
    client = Client()
    answer = client.ask("What is RAG?")
    print(answer)