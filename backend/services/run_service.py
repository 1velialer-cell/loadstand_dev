from datetime import datetime
from backend.db.models.run import TestRun
from backend.models.schemas import RunStatus
from backend.services.run_executor import run_executor

class RunService:
    def __init__(self, run_repo, result_repo):
        self.run_repo = run_repo
        self.result_repo = result_repo

    async def create_run(self, tool_name: str):
        run = TestRun(tool_name=tool_name, status=RunStatus.CREATED.value)
        run = self.run_repo.create(run)
        run_executor.start_run(run.id, tool_name)
        return run