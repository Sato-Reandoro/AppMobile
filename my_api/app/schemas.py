from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    user_type: str

class User(UserBase):
    id: int
    user_type: str


#agendamento
class ScheduleBase(BaseModel):
    name: Optional[str]
    condominium: Optional[str]
    date_time: Optional[datetime]

class ScheduleCreate(ScheduleBase):
    name: str
    condominium: str
    date_time: datetime

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    condominium: Optional[str] = None
    date_time: Optional[datetime] = None

class Schedule(ScheduleBase):
    id: int
    owner_id: int  # Renomeado de user_id para owner_id

    class Config:
        orm_mode = True