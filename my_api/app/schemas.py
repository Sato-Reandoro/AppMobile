from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    user_type: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    user_type: str

    class Config:
        orm_mode = True


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
    owner_id: int

    class Config:
        orm_mode = True

class FormBase(BaseModel):
    title: Optional[str]
    description: Optional[str]

class FormCreate(FormBase):
    title: str
    description: str

class Form(FormBase):
    id: int
    schedule_id: int

    class Config:
        orm_mode = True

class FormUpdate(FormBase):
    title: Optional[str] = None
    description: Optional[str] = None