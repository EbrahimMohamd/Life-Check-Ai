from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.models import User, MedicalRecord
from ..schemas.auth import RecordCreate, RecordResponse, PasswordChange
from .auth import get_password_hash, verify_password
from jose import jwt, JWTError
import json

router = APIRouter(prefix="/patient", tags=["patient"])

SECRET_KEY = "my_super_secret_offline_key_for_lifecheck_platform_expert"
ALGORITHM = "HS256"

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if not authorization:
        raise credentials_exception
        
    try:
        token = authorization.split(" ")[1] if " " in authorization else authorization
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/records", response_model=RecordResponse)
def save_record(record: RecordCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_record = MedicalRecord(
        patient_id=current_user.id,
        record_type=record.record_type,
        data_json=record.data_json
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/records", response_model=List[RecordResponse])
def get_my_records(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(MedicalRecord).filter(MedicalRecord.patient_id == current_user.id).order_by(MedicalRecord.created_at.desc()).all()
    return records
    
@router.get("/profile")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "full_name": current_user.full_name,
        "age": current_user.age,
        "gender": current_user.gender,
        "email": current_user.email,
        "username": current_user.username,
        "registered_at": current_user.created_at
    }

@router.delete("/records")
def clear_my_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(MedicalRecord).filter(MedicalRecord.patient_id == current_user.id).delete()
    db.commit()
    return {"message": "All medical history cleared successfully"}

@router.delete("/account")
def delete_my_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(User).filter(User.id == current_user.id).delete()
    db.commit()
    return {"message": "Account deleted successfully"}

@router.put("/password")
def change_password(payload: PasswordChange, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
        
    current_user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
