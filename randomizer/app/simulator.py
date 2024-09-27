import asyncio
from datetime import datetime
from typing import Union
from sqlalchemy.orm import Session
from .models import LLM, Metric, Simulation
from .llm_factory.fake_llm_factory import FakeLLMFactory
from .llm_factory.real_llm_factory import RealLLMFactory

# Number of queries to send (1000 data points)
num_queries = 1000

async def generate_data(db: Session, factory, llms: list, prompt: str, seed):
    tasks = []

    for llm in llms:
        for _ in range(num_queries):
            tasks.append(query_and_store_metrics(db, llm, prompt, factory, seed))

    await asyncio.gather(*tasks)

async def query_and_store_metrics(db: Session, llm_name: str, prompt: str, factory: Union[RealLLMFactory, FakeLLMFactory], seed):
    try:
        result = await factory.generate_metrics(llm_name, prompt=prompt, seed=seed)

        record_simulation(db, llm_name, "TTFT", result["ttft"])
        record_simulation(db, llm_name, "TPS", result["tps"])
        record_simulation(db, llm_name, "e2e_latency", result["e2e_latency"])

    except Exception as e:
        print(f"Error querying model {llm_name}: {e}")

# Store the simulation results in the PostgreSQL database
def record_simulation(db: Session, llm_name: str, metric_name: str, value: float):
    llm = db.query(LLM).filter(LLM.name == llm_name).first()
    metric = db.query(Metric).filter(Metric.name == metric_name).first()

    if not llm:
        llm = LLM(name=llm_name)
        db.add(llm)
        db.commit()
        db.refresh(llm)

    if not metric:
        metric = Metric(name=metric_name)
        db.add(metric)
        db.commit()
        db.refresh(metric)

    simulation = Simulation(
        llm_id=llm.id,
        metric_id=metric.id,
        value=value,
        recorded_at=datetime.utcnow()
    )

    db.add(simulation)
    db.commit()
    db.refresh(simulation)

    print(f"Recorded: {llm_name} - {metric_name}: {value}")
