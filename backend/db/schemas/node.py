from pydantic import BaseModel
from backend.db.models.enums import NodeRole

class NodeCreate(BaseModel):
    name: str
    host: str
    port: int
    role: NodeRole
    ssh_login: str | None = None
    ssh_password: str | None = None

class NodeUpdate(BaseModel):
    name: str | None = None
    host: str | None = None
    port: int | None = None
    role: NodeRole | None = None
    ssh_login: str | None = None
    ssh_password: str | None = None