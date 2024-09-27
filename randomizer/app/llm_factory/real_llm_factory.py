from .llm_interface import LLMFactory
from ..model_query import query_ollama_model

class RealLLMFactory(LLMFactory):
    async def generate_metrics(self, llm_name: str, prompt: str):
        return await query_ollama_model(llm_name, prompt)
