from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from typing import List
from time import time

from app.database import engine, get_db
from app.models import Base
from app.routers import auth, decisions, analysis

app = FastAPI(title="Human Free-Will Erosion Engine")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(decisions.router)
app.include_router(analysis.router)