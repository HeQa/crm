from pydantic import BaseModel
from typing import List, Optional


class ScriptsResponse(BaseModel):
    id: int
    name: str
    description: str

class ScriptsTextResponse(BaseModel):
    id: int
    script: int
    parent: int
    head: int
    text: str

class ScriptNodeRequest(BaseModel):
    script: ScriptsResponse
    script: List[ScriptsTextResponse] = []

class ScriptRequest(BaseModel):
    id: int
    parent: int = 0

# ---------------------------------------------------------------

class ScriptCreate(BaseModel):
    name: str
    description: Optional[str]

class ScriptUpdate(BaseModel):
    id: int
    name: str
    description: Optional[str]

class ScriptDelete(BaseModel):
    id: int

class ScriptTextCreate(BaseModel):
    script_id: int
    parent: int = 0
    head: str
    text: str

class ScriptTextUpdate(BaseModel):
    id: int
    head: Optional[str] = None
    text: Optional[str] = None

class ScriptTextDelete(BaseModel):
    id: int
