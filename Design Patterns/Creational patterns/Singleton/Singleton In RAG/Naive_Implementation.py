'''
1. Problem Statement (Real System)

You are building a RAG pipeline:

Client → API → Retriever → LLM → Response
                    ↓
                 Logging

You want:

Every component logs
All logs go to the same place
No duplicate logger instances
'''

import time


class Logger:
    def __init__(self):
        print("Logger initialized")

    def log(self, message):
        print(f"[LOG] {message}")


class Retriever:
    def retrieve(self, query):
        logger = Logger()  # ❌ new instance every time
        logger.log(f"Retrieving documents for: {query}")
        time.sleep(1)
        return ["doc1", "doc2"]


class LLM:
    def generate(self, query, docs):
        logger = Logger()  # ❌ new instance again
        logger.log(f"Generating answer for: {query}")
        time.sleep(1)
        return "final answer"


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLM()

    def run(self, query):
        logger = Logger()  # ❌ again new instance
        logger.log(f"Pipeline started for: {query}")

        docs = self.retriever.retrieve(query)
        answer = self.llm.generate(query, docs)

        logger.log("Pipeline finished")
        return answer


pipeline = RAGPipeline()
pipeline.run("What is RAG?")

'''
Problem with this implementation:

   Multiple logger instances
   Repeated initialization
   Hard to redirect logs (file, DB, etc.)
   No central control

At scale:
   1000 requests → 3000 logger objects

'''