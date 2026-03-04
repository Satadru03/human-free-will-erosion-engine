from sqlalchemy.orm import Session
from app.models import User, DecisionEvent, DailySummary
from app.analysis.markov import Predict

from datetime import datetime, date

def create_user(db: Session, user, password_hash):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return None
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=password_hash
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def login(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user.password

def create_event(db: Session, owner_id = int, occurred_at: datetime, domain: str, action: str):
    decisionevent = DecisionEvent(
        occurred_at=occurred_at,
        owner_id=owner_id,
        domain=domain,
        action=action
    )

    db.add(decisionevent)
    db.commit()
    db.refresh(decisionevent)
    return decisionevent

def get_decision_events(db: Session, username: str):
    return db.query(DecisionEvent).filter(DecisionEvent.owner == username).all()

def create_dailysummary(db: Session, username: str, date: date, entropy_score: float, predictability_score: float, free_will_index: float):
    dailysummary = DailySummary(
        date=date,
        decision_count=count,
        entropy_score=entropy_score,
        predictability_score=predictability_score,
        free_will_index=free_will_index
    )

    db.add(dailysummary)
    db.commit()
    db.refresh(dailysummary)
    return dailysummary

def get_summary(db: Session, owner: int, days: int, note: str):
    dailysummary = DailySummary(
        days = [],
        note = "Metrics computed in later phase"
    )
    return db.query(DailySummary).filter(DailySummary.owner_id == owner).all()

def get_predict_next(db: Session, owner: int):
    predict = Predict(
        next_action = null,
        confidence = null,
        reason = "Markov model not initialized (requires ≥ N transitions)"
    )
    return predict
