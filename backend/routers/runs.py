from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.repositories.run_repository import RunRepository
from backend.repositories.result_repository import RunResultRepository
from backend.services.run_service import RunService
from backend.models.schemas import (RunCreate,RunRead,)

router = APIRouter(
    prefix="/runs",
    tags=["runs"],
)

@router.post("")
async def create_run(payload: RunCreate,db: Session = Depends(get_db),):
    run_repo = RunRepository(db)
    result_repo = RunResultRepository(db)
    service = RunService(run_repo,result_repo,)
    run = await service.create_run(payload.tool_name)
    return {"id": run.id,"tool_name": run.tool_name,"status": run.status,}

@router.get("")
async def get_runs(db: Session = Depends(get_db),):
    repo = RunRepository(db)
    return repo.list()
    return {"id": run.id,"tool_name": run.tool_name,"status": run.status,}

@router.get("/{run_id}")
async def get_run(run_id: str,db: Session = Depends(get_db),):
    repo = RunRepository(db)
    run = repo.get(run_id)
    if not run:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )
    return {"id": run.id,"tool_name": run.tool_name,"status": run.status,}

@router.get("/{run_id}/result")
async def get_result(run_id: str,db: Session = Depends(get_db),):
    repo = RunResultRepository(db)
    result = repo.get_by_run(run_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not found",
        )
    return result