from pydantic import BaseModel
from typing import Optional, Dict, Any

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