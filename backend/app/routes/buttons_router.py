from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from app.schemas import (ButtonsResponse, ButtonRequest, ButtonNodeRequest,
                         ButtonRequest, ButtonCreate, ButtonUpdate,
                         ButtonDelete)
from typing import List
from app.auth.dependencies import get_current_user
from app.services.buttons_service import (get_buttons_all)

router = APIRouter(prefix="/buttons", tags=["Scripts"])

@router.get("/get", response_model=List[ButtonsResponse])
async def get_script_roots(
user=Depends(get_current_user)
):
    scripts = await get_buttons_all()
    return scripts