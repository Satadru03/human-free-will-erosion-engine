from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List
import math

from app.database import get_db
from app.routers.auth import get_current_user
from app.schema import DailySummaryRead, Predict
from app import crud

from app.analysis.markov import predict_next_action
from app.analysis.entropy import calculate_entropy
from app.analysis.simulation import simulate_future, find_dominant_loop, simulated_predictability
from app.analysis.metrics import free_will_index

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/history")
def get_events_history(start_date: date | None = Query(default=None), end_date: date | None = Query(default=None), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if start_date is None and end_date is None:
        start_date = date.today()
        end_date = date.today()

    events = crud.get_decisions_between_dates(db=db, owner_id=current_user.id, start_date=start_date, end_date=end_date)

    if not events:
        return []

    results = []

    for e in events:
        results.append({
            "id": e.id,
            "action": e.action,
            "domain": e.domain,
            "timestamp": e.occurred_at
        })
        
    return results

@router.get("/today", response_model=DailySummaryRead)
def get_analysis_today(target_date: date | None = Query(default=None), current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    if target_date is None:
        target_date = date.today()

    events = crud.get_decisions_by_day(db, owner_id=current_user.id, target_date=target_date)

    if not events:
        return {
            "date": target_date,
            "entropy_score": 0,
            "predictability_score": None,
            "free_will_index": None
        }

    unique_actions = len({e.action for e in events})

    entropy_score = calculate_entropy(events)

    if unique_actions <= 1:
        predictability_score = None
    else:
        predictability_score = round(1 - entropy_score / math.log2(unique_actions), 3)
    
    next_action, confidence = predict_next_action(events)

    fwi = free_will_index(entropy_score, unique_actions, confidence)

    return {
        "date": target_date,
        "entropy_score": entropy_score,
        "predictability_score": predictability_score,
        "free_will_index": fwi
    }

@router.get("/summary", response_model=List[DailySummaryRead])
def get_summary(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    events = crud.get_decision_events(db, current_user.id)

    if not events:
        return []

    events_by_day = {}

    for e in events:
        day = e.occurred_at.date()
        events_by_day.setdefault(day, []).append(e)

    results = []

    for day, day_events in sorted(events_by_day.items()):

        entropy_score = calculate_entropy(day_events)

        unique_actions = len({e.action for e in day_events})

        if len(day_events) < 2:
            predictability_score = None
        elif unique_actions <= 1:
            predictability_score = 1.0
        else:
            predictability_score = round(
                1 - entropy_score / math.log2(unique_actions), 3
            )
        
        next_action, confidence = predict_next_action(day_events)

        fwi = free_will_index(entropy_score, unique_actions, confidence)

        results.append({
            "date": day,
            "entropy_score": entropy_score,
            "predictability_score": predictability_score,
            "free_will_index": fwi
        })

    return results

@router.get("/predict-next", response_model=Predict)
def get_predict_next(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    events = crud.get_decision_events(db, current_user.id)
    next_action, confidence = predict_next_action(events)

    if next_action is None:
        return {
            "next_action": None,
            "confidence": None,
            "reason": "Markov model not initialized (requires ≥ N transitions)"
        }

    return {
        "next_action": next_action,
        "confidence": confidence,
    }

@router.get("/simulate")
def simulate_behavior(steps: int = 10, current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    events = crud.get_decision_events(db, current_user.id)
    simulated = simulate_future(events, steps)
    dominant_loop = find_dominant_loop(simulated)
    predictability = simulated_predictability(simulated)

    return {
        "predictability_24h": predictability,
        "dominant_loop": dominant_loop,
        "simulated_sequence": simulated
    }