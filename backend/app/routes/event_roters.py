from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from app.schemas import (EventCreate, EventUpdate, EventDelete, EventRespone)
from typing import List
from app.services.event_service import get_event_to_date, event_create, event_update, event_delete
from app.auth.dependencies import get_current_user
from fastapi import Query
from datetime import date
from typing import Optional

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[Optional[EventRespone]])
async def get_event(
        start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
        end_date: Optional[date] = Query(None, description="End date in YYYY-MM-DD format"),
        user=Depends(get_current_user)
):
    event_ = await get_event_to_date(start_date, end_date)
    return event_


@router.post("/event-create", response_model=List[EventRespone])
async def event_create_r(
        event: EventCreate,
        user=Depends(get_current_user)
):
    event_ = await event_create(event)
    return event_


@router.post("/event-update", response_model=List[EventRespone])
async def event_update_r(
        event: EventUpdate,
        user=Depends(get_current_user)
):
    event_ = await event_update(event)
    return event_


@router.delete("/event-delete", response_model=List[Optional[EventRespone]])
async def event_delete_r(
        event: EventDelete,
        user=Depends(get_current_user)
):
    event_ = await event_delete(event)
    return event_

