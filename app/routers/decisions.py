from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app import crud
from app.schema import DecisionEventCreate, DecisionEventRead, get_time_bucket, WeekdayEnum, DecisionDomainEnum
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/decision",
    tags=["Decision"]
)

@router.post("/log", response_model=DecisionEventRead, status_code=status.HTTP_201_CREATED)
def log_decision(event: DecisionEventCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    db_event = crud.create_event(
        db=db,
        owner_id=current_user.id,
        occurred_at=event.occurred_at,
        domain=event.domain.value,
        action=event.action
    )

    if not db_event:
        raise HTTPException(
            status_code=400,
            detail="Could not log decision"
        )

    timebucket = get_time_bucket(db_event.occurred_at)
    weekday = WeekdayEnum[db_event.occurred_at.strftime("%A")]

    return DecisionEventRead(
        id=db_event.id,
        occurred_at=db_event.occurred_at,
        domain=DecisionDomainEnum(db_event.domain),
        action=db_event.action,
        timebucket=timebucket,
        weekday=weekday
    )