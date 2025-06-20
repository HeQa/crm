from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from app.database.models import Employees
from app.schemas import EmployeeCreate, EmployeeLogin, ClientCreate, CallCreate, EventCreate
from typing import List

router = APIRouter(prefix="/employee", tags=["Employee"])



