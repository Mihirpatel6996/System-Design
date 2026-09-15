class LLMService:

    def generate(self, provider, prompt):

        if provider == "gemini":
            return self._call_gemini(prompt)

        elif provider == "groq":
            return self._call_groq(prompt)

        elif provider == "hf":
            return self._call_hf(prompt)

        else:
            raise ValueError("Unknown provider")

    def _call_gemini(self, prompt):
        return f"Gemini response for {prompt}"

    def _call_groq(self, prompt):
        return f"Groq response for {prompt}"

    def _call_hf(self, prompt):
        return f"HF response for {prompt}"


'''
*** Why This Will Break (Real Production Thinking)

Answer this honestly:

What happens when you add OpenAI / Claude / Local LLM?
What happens when fallback logic becomes:
Retry 3 times
Timeout-based switching
Cost-based routing
What happens when different providers need different payload formats?

You’ll keep editing this class.

This becomes a critical failure point.

'''