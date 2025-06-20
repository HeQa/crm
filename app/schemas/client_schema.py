from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas import EmployeeRespone
from datetime import date, time, datetime
from typing import List

class ClientCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    status_id: int
    responsible_employee_id: int
    source: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    responsible_employee: EmployeeRespone
    source: str

class SyncClient(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    status_id: int
    responsible_employee_id: int
    source: Optional[str] = None

class SyncRequest(BaseModel):
    clients: List[SyncClient]