#### Apply OCP Properly ####

# Abstraction - one interface and multiple implementations
from abc import ABC, abstractmethod

class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass


# Concrete Providers 

class GeminiProvider(LLMProvider):

    def generate(self, prompt):
        return f"Gemini response for {prompt}"

class GroqProvider(LLMProvider):

    def generate(self, prompt):
        return f"Groq response for {prompt}"

class HFProvider(LLMProvider):

    def generate(self, prompt):
        return f"HF response for {prompt}"

# Fallback System - Open for extension, closed for modification

class FallbackLLMService:

    def __init__(self, providers):
        self.providers = providers  # ordered list

    def generate(self, prompt):

        for provider in self.providers:
            try:
                return provider.generate(prompt)
            except Exception:
                continue

        raise Exception("All providers failed")