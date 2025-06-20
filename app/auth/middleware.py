from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from auth.dependencies import get_current_user
from database.models.user import User


async def auth_middleware(request: Request, call_next):
    # Исключаем страницы входа и регистрации
    if request.url.path in ['/login', '/register']:
        return await call_next(request)

    try:
        # Проверяем токен
        token = request.cookies.get("access_token") or request.headers.get("Authorization")
        if not token:
            return RedirectResponse(url="/login")

        user = await get_current_user(token)
        request.state.user = user
        return await call_next(request)

    except HTTPException as e:
        return RedirectResponse(url="/login")