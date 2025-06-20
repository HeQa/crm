from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, time, datetime


class CallCreate(BaseModel):
    client_id: int
    employee_id: int
    start_time: datetime
    duration: int
    transcript: Optional[str] = None
    summary: Optional[str] = None
    file_link: Optional[str] = None
    rating: Optional[int] = None