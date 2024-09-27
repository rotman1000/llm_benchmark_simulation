from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import get_db, create_tables
from .simulator import generate_data
from .llm_factory.real_llm_factory import RealLLMFactory
from .llm_factory.fake_llm_factory import FakeLLMFactory

app = FastAPI()

# Example list of LLMs to use
llms = ["GPT-4o", "Llama 3.1", "Mistral Large"]
prompt = "Benchmark test for language model"

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/generate")
async def generate_data_endpoint(
    db: Session = Depends(get_db),
    factory_type: str = Query("fake"),
    seed: str = Query(None)
):
    # Choose the factory based on the query parameter
    if factory_type == "real":
        factory = RealLLMFactory()
    else:
        factory = FakeLLMFactory()

    # Generate the data using the chosen factory
    await generate_data(db, factory, llms, prompt, seed)

    return {"message": f"1,000 data points generated using {factory_type} factory"}
