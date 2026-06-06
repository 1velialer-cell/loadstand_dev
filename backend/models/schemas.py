from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from typing import Literal

class Creds(BaseModel):
    username: str
    password: str

class ToolRunRequest(BaseModel):
    name: str

class ToolResult(BaseModel):
    status: str
    returncode: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None

class ServerCreate(BaseModel):
    name: str
    host: str
    ssh_login: str
    ssh_password: str
    type: Literal["media", "load"]

class Server(ServerCreate):
    id: str

class ServerDelete(BaseModel):
    id: str

class ServerPatch(BaseModel):
    id: str
    name: str | None = None
    host: str | None = None
    ssh_login: str | None = None
    ssh_password: str | None = None
    type: Literal["media", "load"] | None = None