from abc import ABC, abstractmethod

class LLMFactory(ABC):
    @abstractmethod
    async def generate_metrics(self, llm_name: str, prompt: str=None, seed=None):
        pass
