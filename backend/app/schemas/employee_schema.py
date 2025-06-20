from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time, datetime

class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = Field(..., pattern="^(телефонист|менеджер|администратор)$")
    telegram: Optional[str] = None

class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str

class EmployeeRespone(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str = Field(..., pattern="^(телефонист|менеджер|администратор)$")
    telegram: Optional[str] = None,