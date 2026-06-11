from sqlalchemy.orm import Session
from backend.db.models.run import RunResult

class RunResultRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self, result: RunResult):
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result
    def get_by_run(self, run_id: str):
        return (
            self.db.query(RunResult)
            .filter(RunResult.run_id == run_id)
            .first()
        )