from pydantic import BaseModel
from typing import Optional


class ButtonsResponse(BaseModel):
    id: int
    text: str

class ButtonRequest(BaseModel):
    id: int
    parent: int = 0

class ButtonNodeRequest(BaseModel):
    script: ButtonsResponse

class ButtonRequest(BaseModel):
    id: int
    parent: int = 0

# ---------------------------------------------------------------

class ButtonCreate(BaseModel):
    text: str
    description: Optional[str]

class ButtonUpdate(BaseModel):
    id: int
    text: str

class ButtonDelete(BaseModel):
    id: int