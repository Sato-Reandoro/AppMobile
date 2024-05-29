from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    user_type = Column(String)

    schedules = relationship("Schedule", back_populates="owner")

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    condominium = Column(String, index=True)
    date_time = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Renomeado de user_id para owner_id

    owner = relationship("User", back_populates="schedules")