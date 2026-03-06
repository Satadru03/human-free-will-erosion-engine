from datetime import datetime, timedelta
import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.database import get_db
from app import crud
from app.schema import UserCreate, Token, APIResponse
import app.logging_config as logging_config
from app.logging_config import logger

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info("JWT token created")

    return token

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try:
        payload = decode_token(token)
        username = payload.get("sub")

        if username is None:
            logger.warning("Token missing subject")
            raise HTTPException(status_code=401, detail="Invalid token")

        user = crud.get_user(db, username)

        if user is None:
            logger.warning("User from token not found")
            raise HTTPException(status_code=401, detail="Invalid token")

        return user

    except JWTError:
        logger.warning("Invalid or expired JWT token")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=APIResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    password_hash = hash_password(user.password)

    result = crud.create_user(db, user, password_hash)

    if result is None:
        logger.warning(f"Registration attempt failed (user exists): {user.username}")
        raise HTTPException(status_code=409, detail="User already exists")

    logger.info(f"User registered successfully: {user.username}")

    return {
        "status": "success",
        "message": "User created",
        "data": result
    }

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = crud.get_user(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        logger.warning(f"Failed login attempt: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    logger.info(f"User login successful: {form_data.username}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }