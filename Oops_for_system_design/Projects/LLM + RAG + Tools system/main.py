### Abstraction ####

## LLM Interface
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


## RAG Interface

class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass

# Tools Interface

class Tool(ABC):
    @abstractmethod
    def execute(self, input_data: str) -> str:
        pass

##### Inheritance - concrete implementation ####

# LLM implementations

class GeminiLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Gemini]: {prompt}"


class GroqLLM(LLM):
    def generate(self, prompt: str) -> str:
        return f"[Groq]: {prompt}"

# Retriever implementations

class SimpleRetriever(Retriever):
    def retrieve(self, query: str) -> str:
        return f"Context for: {query}"

# Tool implementations

class CalculatorTool(Tool):
    def execute(self, input_data: str) -> str:
        return f"Calculated result for {input_data}"


# Encapsulation — Control internal workflow


class RAGPipeline: # Now we build a pipeline/orchestrator
    def __init__(self, llm: LLM, retriever: Retriever, tools: list[Tool]):
        self._llm = llm
        self._retriever = retriever
        self._tools = tools

    def query(self, user_query: str) -> str:
        context = self._retrieve_context(user_query)
        enriched_prompt = self._build_prompt(user_query, context)
        return self._generate_response(enriched_prompt)

    def _retrieve_context(self, query):
        return self._retriever.retrieve(query)

    def _build_prompt(self, query, context):
        return f"Context: {context}\nQuery: {query}"

    def _generate_response(self, prompt):
        return self._llm.generate(prompt)


'''
This is a simple RAG pipeline that demonstrates the use of LLM, Retriever, and Tools.
It shows how to encapsulate the workflow and manage the interactions between different components.

What is encapsulated here?
How retrieval works
How prompt is built
How LLM is called
'''

##### Polymorphism - interchangeable components - Plug-and-play behavior ####

pipeline1 = RAGPipeline(GeminiLLM(), SimpleRetriever(), [])
pipeline2 = RAGPipeline(GroqLLM(), SimpleRetriever(), [])

pipeline1.query("What is AI?")
pipeline2.query("What is AI?")






