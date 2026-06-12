import uuid
from sqlalchemy import String, Integer, Enum, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from backend.db.base import Base
from backend.db.models.enums import NodeRole, NodeStatus

class Node(Base):
    __tablename__ = "nodes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    role = mapped_column(Enum(NodeRole, name="noderole"), nullable=False)
    status = mapped_column(Enum(NodeStatus, name="nodestatus"), default=NodeStatus.UNKNOWN)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ssh_login = mapped_column(String(128), nullable=True)
    ssh_password = mapped_column(String(128), nullable=True)
    enabled = mapped_column(Boolean, default=True)