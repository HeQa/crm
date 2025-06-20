from fastapi import APIRouter

from app.routes.auth import router as auth_roter
from app.routes.call_router import router as call_router
from app.routes.script_router import router as script_router
from app.routes.event_roters import router as event_roters
from app.routes.clients_router import router as clients_router
from app.routes.employee_router import router as employee_router






router = APIRouter()
router.include_router(auth_roter)
router.include_router(call_router)
router.include_router(script_router)
router.include_router(event_roters)
router.include_router(clients_router)
router.include_router(employee_router)
