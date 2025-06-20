from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class EventCreate(BaseModel):
    client_id: int
    employee_id: int
    event_type: str
    event_date: date
    event_time: time
    description: Optional[str] = None
    status: Optional[str] = None
    mark: Optional[str] = None

class EventUpdate(BaseModel):
    id: int
    event_type: Optional[str] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None
    description: Optional[str] = None
    status: Optional[str] = None
    mark: Optional[str] = None

class EventDelete(BaseModel):
    id: int

class EventRespone(BaseModel):
    id: int
    client_id: int
    employee_id: int
    event_type: str
    event_date: date
    event_time: time
    description: Optional[str] = None
    status: Optional[str] = None
    mark: Optional[str] = None

