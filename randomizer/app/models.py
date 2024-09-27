import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class LLM(Base):
    __tablename__ = 'llms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Simulation(Base):
    __tablename__ = 'simulations'
    id = Column(Integer, primary_key=True, index=True)
    llm_id = Column(Integer, ForeignKey('llms.id'), nullable=False)
    metric_id = Column(Integer, ForeignKey('metrics.id'), nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    llm = relationship("LLM")
    metric = relationship("Metric")
