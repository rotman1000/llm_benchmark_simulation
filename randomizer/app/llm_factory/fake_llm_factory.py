import random
import time
from .llm_interface import LLMFactory

class FakeLLMFactory(LLMFactory):
    async def generate_metrics(self, llm_name: str, prompt, seed):
        if seed is not None:
            random.seed(seed)
        # Simulate fake random metrics
        start_time = time.time()
        ttft = random.uniform(0.1, 2.0)  # Fake Time to First Token (TTFT)
        tps = random.uniform(10, 100)    # Fake Tokens Per Second (TPS)
        e2e_latency = random.uniform(0.5, 5.0)  # Fake End-to-End Latency (e2e_latency)
        
        return {
            "model": llm_name,
            "ttft": ttft,
            "tps": tps,
            "e2e_latency": e2e_latency
        }
