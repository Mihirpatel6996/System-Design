# Definition : High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

# DIP violation 

class GeminiProvider:
    def generate(self, prompt):
        return "Gemini response"


class RAGService:

    def __init__(self):
        self.llm = GeminiProvider()   # X direct dependency

    def answer(self, query):
        return self.llm.generate(query)

'''
Why This Is Bad

Answer these:
    Want to switch to Groq? → modify RAGService 
    Want fallback (Gemini → Groq)? → rewrite logic 
    Want testing (mock LLM)? → hard 
'''

# Core FIX 

# Step 1: Introduce an abstraction

from abc import ABC, abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass

# Step 2 — Implement Low-Level Modules

class GeminiProvider(LLMProvider):
    def generate(self, prompt):
        return "Gemini response"

class GroqProvider(LLMProvider):
    def generate(self, prompt):
        return "Groq response"

# Step 3 — High-Level Module Depends on Abstraction

class RAGService:

    def __init__(self, llm: LLMProvider):   # ✅ abstraction
        self.llm = llm

    def answer(self, query):
        return self.llm.generate(query)

# Step 4 — Inject Dependency

llm = GeminiProvider()
rag = RAGService(llm)

rag.answer("patient risk")

# what changed : 
# 1. RAGService no longer depends on a specific LLM provider. It depends on the abstraction LLMProvider.
# 2. We can now easily switch to a different provider (like GroqProvider)

'''

Before:

RAGService → GeminiProvider

After:

RAGService → LLMProvider ← GeminiProvider
                               ↑
                            GroqProvider
'''