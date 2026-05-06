from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    full_name: Optional[str]

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class RecordCreate(BaseModel):
    record_type: str
    data_json: str

class RecordResponse(RecordCreate):
    id: int
    patient_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
