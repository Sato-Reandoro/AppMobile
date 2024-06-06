from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)

    schedules = relationship("Schedule", back_populates="owner")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    condominium = Column(String, index=True)
    date_time = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Boolean, default=False)

    owner = relationship("User", back_populates="schedules")
    forms = relationship("Form", back_populates="schedule", cascade="all, delete-orphan")

class Form(Base):
    __tablename__ = "forms"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    
    schedule = relationship("Schedule", back_populates="forms")