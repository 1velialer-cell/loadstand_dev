from backend.db.base import Base
from backend.db.session import engine
from backend.db.models.node import Node
from backend.db.models.run import TestRun, RunResult

def init_db():
    Base.metadata.create_all(bind=engine)