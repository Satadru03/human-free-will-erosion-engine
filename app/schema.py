from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, date
from typing import Optional
from enum import Enum
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

class WeekdayEnum(str, Enum):
    Sunday = "Sunday"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"

class DecisionDomainEnum(str, Enum):
    sleep = "sleep"
    work = "work"
    movement = "movement"
    leisure = "leisure"
    health = "health"
    food = "food"
    social = "social"
    entertainment = "entertainment"

class TimeBucketEnum(str, Enum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"
    night = "night"
    late_night = "late_night"

def get_time_bucket(dt: datetime) -> TimeBucketEnum:
    hour = dt.hour

    if 5 <= hour < 12:
        return TimeBucketEnum.morning
    elif 12 <= hour < 17:
        return TimeBucketEnum.afternoon
    elif 17 <= hour < 21:
        return TimeBucketEnum.evening
    elif 21 <= hour < 24:
        return TimeBucketEnum.night
    else:
        return TimeBucketEnum.late_night

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(v) > 64:
            raise ValueError("Password too long")
        return v
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v  

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[UserRead] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class DecisionEventCreate(BaseModel):
    occurred_at: datetime
    domain: DecisionDomainEnum
    action: str

    @field_validator("occurred_at")
    @classmethod
    def validate_occurred_at(cls, v):
        if v.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")

        v_ist = v.astimezone(IST)

        now = datetime.now(IST)

        if v_ist > now:
            raise ValueError("occurred_at cannot be in the future")

        if (now - v_ist).days > 14:
            raise ValueError("occurred_at too far in the past")

        return v_ist

    @field_validator("action")
    @classmethod
    def validate_action(cls, v):
        if len(v) < 2:
            raise ValueError("Action too short")
        if len(v) > 50:
            raise ValueError("Action too long")
        return v
    
class DecisionEventRead(BaseModel):
    id: int
    occurred_at: datetime
    #logged_at: datetime
    domain: DecisionDomainEnum
    action: str
    timebucket: TimeBucketEnum
    weekday: WeekdayEnum
    class Config:
        from_attributes = True

class DailySummaryRead(BaseModel):
    date: date
    entropy_score: Optional[float]
    predictability_score: Optional[float]
    free_will_index: Optional[float]

class Predict(BaseModel):
    next_action: str | None
    confidence: float | None
    reason: Optional[str] = None

    model_config = {
        "exclude_none": True
    }