from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from app.database.models import Employees
from app.schemas import EmployeeCreate, EmployeeRespone
from app.config import config  # Измененный импорт
from app.services.employees_service import employe_respone
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str) -> Optional[Employees]:
    try:
        user = await Employees.get(email=email)
        if not verify_password(password, user.hashed_password):
            return None
        return user
    except DoesNotExist:
        return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

async def create_user(user_data: EmployeeCreate) -> EmployeeRespone:
    hashed_password = get_password_hash(user_data.password)
    # print(user_data)
    user = await Employees.create(
        full_name=user_data.full_name,
        email=user_data.email,
        # phone=user_data.phone,
        hashed_password=hashed_password,
        telegram=user_data.telegram,
        role=user_data.role
    )
    respone = employe_respone(user)
    return await respone

