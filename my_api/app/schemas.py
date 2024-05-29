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
