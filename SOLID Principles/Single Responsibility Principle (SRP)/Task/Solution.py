'''
EmbeddingService
VectorStore
NoteRepository
Retriever
LLMService
Logger
Orchestrator (important)
'''

class EmbeddingService:
    def embed(self, text):
        # fake embedding
        return [len(text)]
    
class VectorStore:
    def __init__(self):
        self.store = {}

    def retrieve(self, query_embedding):
        best_match = None
        best_score = float("inf")

        for pid, emb in self.store.items():
            score = abs(emb[0] - query_embedding[0])
            if score < best_score:
                best_score = score
                best_match = pid

        return best_match
    
class NoteRepository:
    def __init__(self):
        self.db = {}
        self.vector_store = {}

    def store(self, patient_id, note):
            embedding = self.embed(note)
            self.vector_store[patient_id] = embedding
            self.db[patient_id] = note


class LLMService:
    def call_llm(self, context, query):
            return f"LLM Response based on [{context}] for query [{query}]"

class Logger:
    def log(self, msg):
        print(f"LOG: {msg}")

class Orchestrator:
     
    def __init__(self, embedding_service, vector_store, note_repository, llm_service, logger):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.note_repository = note_repository
        self.llm_service = llm_service
        self.logger = logger

    def run(self, patient_id, note, query):
        self.logger.log("Storing note")
        self.note_repository.store(patient_id, note)

        self.logger.log("Retrieving context")
        query_embedding = self.embedding_service.embed(query)
        best_match_id = self.vector_store.retrieve(query_embedding)
        context = self.note_repository.db.get(best_match_id, "")

        self.logger.log("Calling LLM")
        response = self.llm_service.call_llm(context, query)

        self.logger.log("Done")
        return response

