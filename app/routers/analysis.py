from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.database import get_db
from app.routers.auth import get_current_user
from app.schema import DailySummaryRead, Predict
from app import crud

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@router.get("/today", response_model=List[DailySummaryRead])
def get_analysis_today(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    events = crud.get_decision_events(db, owner_id=1)

    return [{
        "date": date.today(),
        "entropy_score": None,
        "predictability_score": None,
        "free_will_index": None
    }]


@router.get("/summary", response_model=List[DailySummaryRead])
def get_summary(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return []


@router.get("/predict-next", response_model=Predict)
def get_predict_next(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return {
        "next_action": None,
        "confidence": None,
        "reason": "Markov model not initialized (requires ≥ N transitions)"
    }