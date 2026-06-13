from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal
from uuid import UUID
from enum import Enum

class Creds(BaseModel):
    username: str
    password: str

class ToolRunRequest(BaseModel):
    tool_name: str

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
    type: Literal["media","load"] | None = None

class RunStatus(str, Enum):
    CREATED = "CREATED"
    PREPARING = "PREPARING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"

class RunCreate(BaseModel):
    tool_name: str

class RunResponse(BaseModel):
    id: str
    tool_name: str
    status: RunStatus

class RunResultResponse(BaseModel):
    run_id: str
    return_code: int
    stdout: str
    stderr: str
    duration_sec: float

class RunRead(BaseModel):
    id: str
    tool_name: str
    status: str
    class Config:
        from_attributes = True

class NodeCreate(BaseModel):
    name: str
    host: str
    port: int
    role: Literal["MEDIA_SERVER", "LOAD_SERVER"]
    ssh_login: Optional[str] = None
    ssh_password: Optional[str] = None

class NodeUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    role: Optional[Literal["MEDIA_SERVER", "LOAD_SERVER"]] = None
    ssh_login: Optional[str] = None
    ssh_password: Optional[str] = None

class SSHCommandRequest(BaseModel):
    command: str
