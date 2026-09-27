# Singleton Logger

class Logger:
    _instance = None

    def __init__(self):
        print("Logger initialized")

    def log(self, message):
        print(f"[LOG] {message}")


# Eager initialization
Logger._instance = Logger()


def get_logger():
    return Logger._instance


# using it in RAG pipeline

import time


class Retriever:
    def __init__(self):
        self.logger = get_logger()

    def retrieve(self, query):
        self.logger.log(f"Retrieving documents for: {query}")
        time.sleep(1)
        return ["doc1", "doc2"]


class LLM:
    def __init__(self):
        self.logger = get_logger()

    def generate(self, query, docs):
        self.logger.log(f"Generating answer for: {query}")
        time.sleep(1)
        return "final answer"


class RAGPipeline:
    def __init__(self):
        self.logger = get_logger()
        self.retriever = Retriever()
        self.llm = LLM()

    def run(self, query):
        self.logger.log(f"Pipeline started for: {query}")

        docs = self.retriever.retrieve(query)
        answer = self.llm.generate(query, docs)

        self.logger.log("Pipeline finished")
        return answer


pipeline = RAGPipeline()
pipeline.run("What is RAG?")

'''
output:

    Logger initialized
    [LOG] Pipeline started for: What is RAG?
    [LOG] Retrieving documents for: What is RAG?
    [LOG] Generating answer for: What is RAG?
    [LOG] Pipeline finished
'''