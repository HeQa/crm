from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import JSONResponse

from app.auth.dependencies import get_current_user
from app.schemas import Token, EmployeeCreate, EmployeeRespone
from app.services.auth import (
    authenticate_user, create_access_token,
    create_user, get_password_hash, oauth2_scheme
)
from app.database.models.user import (Employees)

from datetime import timedelta
from typing import List
from app.config import config  # Измененный импорт

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=EmployeeRespone)
async def register(user: EmployeeCreate):
    try:
        if not user.full_name.strip():
            raise HTTPException(status_code=400, detail="Full name cannot be empty")
        if await Employees.filter(email=user.email).exists():
            raise HTTPException(status_code=400, detail="Email already registered")
        # if await Employees.filter(phone=user.phone).exists():
        #     raise HTTPException(status_code=400, detail="Phone already registered")

        user_created = await create_user(user)
        return user_created
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response = JSONResponse(
        content={"access_token": access_token}
    )
    response.set_cookie(
        key="access_token",
        value=f"{access_token}",
        httponly=True,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return response


@router.get("/token_validity")
async def register(user=Depends(get_current_user)):
    return {
              "detail": "authenticated"
            }
