from app.database.models import Events
from app.schemas import (EventCreate, EventUpdate, EventDelete, EventRespone)
from typing import List
import datetime


async def event_response(event: Events):
    return EventRespone(
                        id=event.id,
                        client_id=event.client,
                        employee_id=event.employee,
                        event_type=event.event_type,
                        event_date=event.event_date,
                        event_time=event.event_time,
                        description=event.description,
                        status=event.status,
                        mark=event.mark
    )

async def get_event_to_date(start_date: datetime, end_date: datetime) -> List[EventRespone]:
    events = await Events.filter(event_date__gte=start_date, event_date__lte=end_date).all()
    if events:
        return [await event_response(event) for event in events]
    else:
        return []

# -----------------------------------------------------------------

async def event_create(event: EventCreate):
    new_event = await Events.create(
                                    client=event.client_id,
                                    employee=event.employee_id,
                                    event_type=event.event_type,
                                    event_date=event.event_date,
                                    event_time=event.event_time,
                                    description=event.description,
                                    status=event.status,
                                    mark=event.mark
    )

    return await get_event_to_date(start_date=new_event.event_date, end_date=new_event.event_date)

async def event_update(event: EventUpdate):
    update = {}
    if event.event_type:
        update['event_type'] = event.event_type
    if event.event_type:
        update['event_date'] = event.event_date
    if event.event_type:
        update['event_time'] = event.event_time
    if event.event_type:
        update['description'] = event.description
    if event.event_type:
        update['status'] = event.status
    if event.event_type:
        update['mark'] = event.mark

    await Events.update_or_create(
        id=event.id,
        defaults={**update}

    )
    update_event = await Events.get_or_none(id=event.id)
    return await get_event_to_date(start_date=update_event.event_date, end_date=update_event.event_date)


async def event_delete(event: EventDelete):
    delete_event = await Events.get_or_none(id=event.id)
    await Events.filter(id=event.id).delete()
    return await get_event_to_date(start_date=delete_event.event_date, end_date=delete_event.event_date)

