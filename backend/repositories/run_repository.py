from sqlalchemy.orm import Session
from backend.db.models.run import TestRun

class RunRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self, run: TestRun):
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run
    def get(self, run_id: str):
        return self.db.get(TestRun, run_id)
    def list(self):
        return self.db.query(TestRun).all()
    def save(self):
        self.db.commit()
    def update(self, run):
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run