from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    records = relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    record_type = Column(String, index=True) # "Diabetes", "Heart", "Lung", "Chat"
    data_json = Column(Text) # storing results payload
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    patient = relationship("User", back_populates="records")
