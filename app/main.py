from fastapi import FastAPI
from app.schema import UserCreate, UserRead, DecisionEventCreate, DecisionEventRead
#, DailySummaryRead
from app.routers import decisions

app = FastAPI(title = "Human Free-Will Erosion Engine")

app.include_router(decisions.router)