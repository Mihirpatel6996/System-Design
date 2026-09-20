# RAG System components 

# Bad Design 

class LLMService:
    def generate(self):
        pass

    def fine_tune(self):
        pass

    def stream(self):
        pass

    def evaluate(self):
        pass

'''
Problem:
    Not all providers support:
        fine-tuning
        streaming
        evaluation

    So, we have to implement fake methods that raise NotImplementedError for unsupported features. This is a violation of the Interface Segregation Principle (ISP).
'''
## Good Design

class Generator:
    def generate(self):
        pass


class Streamer:
    def stream(self):
        pass


class FineTuner:
    def fine_tune(self):
        pass

class Generator:
    def generate(self):
        pass


class Streamer:
    def stream(self):
        pass


class FineTuner:
    def fine_tune(self):
        pass

