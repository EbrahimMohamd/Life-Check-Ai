from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from ..schemas.auth import UserCreate, UserLogin, Token
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "my_super_secret_offline_key_for_lifecheck_platform_expert"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        gender=user.gender,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user_id": new_user.id, "full_name": new_user.full_name}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_user.id, "full_name": db_user.full_name}
