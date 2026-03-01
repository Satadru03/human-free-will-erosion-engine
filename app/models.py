from sqlalchemy import Column, Integer, String, Float, TIMESTAMPT, DateTime
from sqlalchemy.orm import declarative_base

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
    owner = Column(String, nullable=False)
    occurred_at = Column(TIMESTAMPT, nullable=False)
    logged_at = Column(DateTime, default=func.now())
    domain = Column(String, nullable=False)
    action = Column(String, nullable=False)

# class DailySummary(Base):
#     __tablename__ = "dailysummary"
    
#     id = Column(Integer, primary_key=True, index=True)
#     owner = Column(String, nullable=False)
#     date = Column(DATE, nullable=False)
#     entropy_score = Column(Float, nullable=False)
#     predictability_score = Column(Float, nullable=False)
#     free_will_index = Column(Float, nullable=False)