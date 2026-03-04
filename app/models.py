from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class DecisionEvent(Base):
    __tablename__ = "decisionevent"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False, index=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
    logged_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    domain = Column(String, nullable=False)
    action = Column(String, nullable=False)

class DailySummary(Base):
    __tablename__ = "dailysummary"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, nullable=False)
    entropy_score = Column(Float, nullable=False)
    predictability_score = Column(Float, nullable=False)
    free_will_index = Column(Float, nullable=False)