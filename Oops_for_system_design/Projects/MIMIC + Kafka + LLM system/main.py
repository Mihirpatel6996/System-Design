# Core Interface -- Abstractions

from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass


class Retriever(ABC):
    @abstractmethod
    async def retrieve(self, patient_id: str) -> str:
        pass


class Tool(ABC):
    @abstractmethod
    async def execute(self, data: dict) -> str:
        pass


# concrete implementations

class GeminiLLM(LLM):
    async def generate(self, prompt: str) -> str:
        return f"[Gemini Response]: {prompt}"


class GroqLLM(LLM):
    async def generate(self, prompt: str) -> str:
        return f"[Groq Response]: {prompt}"

# retriever implementations - MIMIC database retrievers

class MIMICRetriever(Retriever):
    async def retrieve(self, patient_id: str) -> str:
        # simulate DB fetch
        return f"Vitals + Notes for patient {patient_id}"

# Tool implementations - Example tools 

class RiskScoreTool(Tool):
    async def execute(self, data: dict) -> str:
        return f"Risk Score: {sum(data.values())}"


# Encapsulation - Orchestration Layer 
# In ClinicalPipeline class the LLM, Retriever, and Tools are encapsulated and orchestrated to provide a seamless interface for clinical queries.
class ClinicalPipeline:
    def __init__(self, llm: LLM, retriever: Retriever, tools: list[Tool]):
        self._llm = llm
        self._retriever = retriever
        self._tools = tools

    async def run(self, patient_id: str, query: str):
        context = await self._get_context(patient_id)
        enriched_prompt = self._build_prompt(query, context)

        if self._needs_tool(query):
            tool_result = await self._execute_tool(context)
            enriched_prompt += f"\nTool Result: {tool_result}"

        return await self._generate(enriched_prompt)

    async def _get_context(self, patient_id):
        return await self._retriever.retrieve(patient_id)

    def _build_prompt(self, query, context):
        return f"Context: {context}\nQuery: {query}"

    def _needs_tool(self, query):
        return "risk" in query.lower()

    async def _execute_tool(self, context):
        for tool in self._tools:
            return await tool.execute({"value": 10})

    async def _generate(self, prompt):
        return await self._llm.generate(prompt)


# Polymorphism - The ClinicalPipeline can work with any LLM, Retriever, or Tool implementation, allowing for flexible and interchangeable components.

pipeline = ClinicalPipeline(
    llm=GeminiLLM(),
    retriever=MIMICRetriever(),
    tools=[RiskScoreTool()]
)

# switch LLM implementation to GroqLLM

pipeline = ClinicalPipeline(
    llm=GroqLLM(),
    retriever=MIMICRetriever(),
    tools=[RiskScoreTool()]
)

## ----------------Kafka Layer (streaming ingestion) --------------

## 1.Producer (data ingestion)

from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_patient_data(data):
    producer.send("patient_topic", data)



## 2. Consumer (processing service)

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "patient_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

for message in consumer:
    data = message.value
    # store in DB or trigger pipeline



