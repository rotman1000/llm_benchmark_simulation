from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import LLM, Metric, Simulation

# Function to get rankings from the database
def get_rankings(db: Session, metric_name: str):
    metric = db.query(Metric).filter(Metric.name == metric_name).first()

    if not metric:
        return {"error": f"Metric '{metric_name}' not found"}

    rankings = (
        db.query(LLM.name, func.avg(Simulation.value).label('mean'))
        .join(Simulation, Simulation.llm_id == LLM.id)
        .filter(Simulation.metric_id == metric.id)
        .group_by(LLM.name)
        .order_by(func.avg(Simulation.value).desc())
        .all()
    )

    formatted_rankings = [{"llm": llm_name, "mean": mean} for llm_name, mean in rankings]

    return {"metric": metric_name, "rankings": formatted_rankings}
