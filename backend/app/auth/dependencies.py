from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from app.database.models.user import Employees
from app.schemas.auth import TokenData
from app.config import config  # Измененный импорт

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
from fastapi import Header, HTTPException

from fastapi import Request, HTTPException


from typing import Optional
async def get_current_user(
    request: Request,
    authorization: Optional[str] = Header(None)  # Берём токен из заголовка
):
    # Пробуем получить токен из заголовка Authorization
    token_from_header = None
    if authorization and authorization.startswith("Bearer "):
        token_from_header = authorization.replace("Bearer ", "")

    # Пробуем получить токен из куки
    token_from_cookie = request.cookies.get("access_token")

    # Выбираем токен (приоритет у заголовка)
    token = token_from_header or token_from_cookie

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (no token provided)",
        )

    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await Employees.get_or_none(email=email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")