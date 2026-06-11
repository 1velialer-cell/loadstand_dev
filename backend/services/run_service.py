from datetime import datetime
from backend.db.models.run import (TestRun,RunResult,)
from backend.models.schemas import RunStatus
from backend.services.tool_executor import run_tool

class RunService:
    def __init__(self,run_repo,result_repo,):
        self.run_repo = run_repo
        self.result_repo = result_repo

    async def create_run(self, tool_name: str):
        run = TestRun(tool_name=tool_name,status=RunStatus.CREATED.value,)
        run = self.run_repo.create(run)
        run.status = RunStatus.RUNNING.value
        run.started_at = datetime.utcnow()
        self.run_repo.save()
        result_data = await run_tool(tool_name)
        run.finished_at = datetime.utcnow()
        run.status = (RunStatus.FINISHED.value
            if result_data["return_code"] == 0
            else RunStatus.FAILED.value
        )
        self.run_repo.save()
        result = RunResult(run_id=run.id,**result_data,)
        self.result_repo.create(result)
        return run