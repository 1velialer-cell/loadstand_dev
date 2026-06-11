from datetime import datetime
import uuid
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from backend.db.base import Base

class TestRun(Base):
    __tablename__ = "test_runs"
    id: Mapped[str] = mapped_column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    tool_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)

class RunResult(Base):
    __tablename__ = "run_results"
    id: Mapped[str] = mapped_column(String(36),primary_key=True,default=lambda: str(uuid.uuid4()))
    run_id: Mapped[str] = mapped_column(String(36),ForeignKey("test_runs.id"),unique=True)
    return_code: Mapped[int] = mapped_column(Integer)
    stdout: Mapped[str] = mapped_column(Text)
    stderr: Mapped[str] = mapped_column(Text)
    duration_sec: Mapped[float] = mapped_column(Float)
