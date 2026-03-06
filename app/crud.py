from sqlalchemy.orm import Session
from app.models import User, DecisionEvent, DailySummary

from datetime import datetime, date, timedelta

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

def create_event(db: Session, owner_id: int, occurred_at: datetime, domain: str, action: str):
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

def get_decision_events(db: Session, owner_id: int):
    return db.query(DecisionEvent).filter(DecisionEvent.owner_id == owner_id).order_by(DecisionEvent.occurred_at).all()

def get_decisions_by_day(db: Session, user_id: int, target_date: date):

    start = datetime.combine(target_date, datetime.min.time())
    end = start + timedelta(days=1)

    return db.query(DecisionEvent).filter(
        DecisionEvent.owner_id == user_id,
        DecisionEvent.occurred_at >= start,
        DecisionEvent.occurred_at < end
    ).order_by(DecisionEvent.occurred_at).all()
