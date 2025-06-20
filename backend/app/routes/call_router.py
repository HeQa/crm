from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from app.database.models import Employees
from app.schemas import EmployeeCreate, EmployeeLogin, ClientCreate, CallCreate, EventCreate, ClientResponse
from typing import List
from app.services.client_service import get_clients_all, create_client_service
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/calls", tags=["Calls"])

