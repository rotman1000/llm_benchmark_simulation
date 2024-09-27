import datetime
from datetime import timedelta
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
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


class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.datetime.utcnow() + timedelta(days=30))  # API key expires in 30 days
    last_used_at = Column(DateTime)
