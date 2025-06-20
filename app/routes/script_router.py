from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from app.schemas import (ScriptsResponse, ScriptRequest, ScriptNodeRequest,
                         ScriptCreate, ScriptUpdate, ScriptDelete,
                         ScriptTextCreate, ScriptTextUpdate, ScriptTextDelete)
from typing import List
from app.auth.dependencies import get_current_user
from app.services.script_service import (get_scripts_all, get_scripts_node, get_scripts_node_back,
                                         script_create, script_update, script_delete,
                                         script_text_create, script_text_update, script_text_delete)

router = APIRouter(prefix="/scripts", tags=["Scripts"])


#
# 1. Получить скрипты
@router.get("/start", response_model=List[ScriptsResponse])
async def get_script_roots(
user=Depends(get_current_user)
):
    scripts = await get_scripts_all()
    return scripts

# 2. Получить узел
@router.get("/node/get", response_model=ScriptNodeRequest)
async def get_script_node(

        script: ScriptRequest,
        user=Depends(get_current_user)
):
    scripts = await get_scripts_node(script)
    return scripts

# 3. Получить верхний узел
@router.get("/node/back", response_model=ScriptNodeRequest)
async def get_script_node_back(
        script: ScriptRequest,
        user=Depends(get_current_user)
):
    scripts = await get_scripts_node_back(script)
    return scripts

# -----------------------------------------------------


# 3. Создать Скрипт
@router.post("/create", response_model=List[ScriptsResponse])
async def get_script_create(
        script: ScriptCreate,
        user=Depends(get_current_user)
):
    scripts = await script_create(script)
    return scripts


# 3. Обновить Скрипт
@router.post("/update", response_model=List[ScriptsResponse])
async def get_script_roots(
        script: ScriptUpdate,
        user=Depends(get_current_user)
):
    scripts = await script_update(script)
    return scripts

# 3. Удалить Скрипт
@router.delete("/delete", response_model=List[ScriptsResponse])
async def get_script_roots(
        script: ScriptDelete,
        user=Depends(get_current_user)
):
    scripts = await script_delete(script)
    return scripts

# -----------------------------------------------------

# 3. Создать Текст в скрипте
@router.post("/text-create", response_model=ScriptNodeRequest)
async def get_script_roots(
        script: ScriptTextCreate,
        user=Depends(get_current_user)
):
    scripts = await script_text_create(script)
    return scripts

# 3. Обновить Текст в скрипте
@router.post("/text-update", response_model=ScriptNodeRequest)
async def get_script_roots(
        script: ScriptTextUpdate,
        user=Depends(get_current_user)
):
    scripts = await script_text_update(script)
    return scripts

# 3. Удалить Текст в скрипте
@router.delete("/text-delete", response_model=ScriptNodeRequest)
async def get_script_roots(
        script: ScriptTextDelete,
        user=Depends(get_current_user)
):
    scripts = await script_text_delete(script)
    return scripts