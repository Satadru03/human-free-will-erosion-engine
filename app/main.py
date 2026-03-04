from fastapi import FastAPI
from app.schema import UserCreate, UserRead, DecisionEventCreate, DecisionEventRead, Token, DailySummaryRead, Predict
from app.routers import decisions
from app.database import engine
from app.models import Base
from app.routers import decisions
from app.auth import hash_password, verify_password, create_access_token, get_current_user
import app.logging_config as logging_config
from app.logging_config import logger
from typing import List

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error: {request.method} {request.url.path}")
        raise
    duration = time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {duration:.2f}s"
    )

    return response

@app.post("/users", response_model = APIResponse, status_code = 201)
def create_user_api(user: UserCreate, db = Depends(get_db)):
    
    password_hash = hash_password(user.password)
    result = crud.create_user(db, user, password_hash)

    if result is None:
        raise HTTPException(status_code=409, detail="User already exists")

    return {
        "status": "success",
        "message": "User created",
        "data": result
    }

@app.post("/login", response_model=Token)
def login_api(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = crud.login(db, form_data.username)

    if not user or not verify_password(form_data.password, user):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
  
app.include_router(decisions.router)

@app.get("/today", response_model = List[DailySummaryRead])
def get_analysis_today_api(current_user: str = Depends(get_current_user), db = Depends(get_db)):
    summary = crud.create_dailysummary(db, current_user, date, decision_count, entropy_score, predictability_score)
    return summary

@app.get("/summary", response_model = List[DecisionEventRead])
def get_summary_api(current_user: str = Depends(get_current_user), db = Depends(get_db)):
    summary = crud.get_dailysummary(db, current_user)
    return summary

@app.get("/predict-next", response_model = List[Predict])
def get_predict_next_api(current_user: str = Depends(get_current_user), db = Depends(get_db)):
    predict = crud.get_predict_next(db, current_user)
    return predict