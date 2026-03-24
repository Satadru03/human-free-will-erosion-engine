from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app import crud
from app.schema import DecisionEventCreate, DecisionEventRead, get_time_bucket, WeekdayEnum, DecisionDomainEnum
from app.routers.auth import get_current_user
from app.utils.domain_mapper import ACTION_DOMAIN_MAP

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
        domain = event.domain.value if event.domain else ACTION_DOMAIN_MAP.get(event.action, "leisure"),
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

@router.put("/{event_id}", response_model=DecisionEventRead)
def update_decision(
    event_id: int,
    event: DecisionEventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    db_event = crud.update_event(
        db=db,
        event_id=event_id,
        owner_id=current_user.id,
        occurred_at=event.occurred_at,
        domain = event.domain.value if event.domain else ACTION_DOMAIN_MAP.get(event.action, "leisure"),
        action=event.action
    )

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

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

@router.delete("/{event_id}")
def delete_decision(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    success = crud.delete_event(
        db=db,
        event_id=event_id,
        owner_id=current_user.id
    )

    if not success:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Decision deleted"}