from app.database.models import Button
from app.schemas import (ButtonsResponse, ButtonRequest, ButtonNodeRequest,
                         ButtonRequest, ButtonCreate, ButtonUpdate,
                         ButtonDelete)
from typing import List

async def button_response(button: Button):
    return ButtonsResponse(
        id=button.id,
        text=button.name)

async def get_buttons_all() -> List[ButtonsResponse]:
    buttons = await Button.all()
    return [await button_response(script) for script in buttons]