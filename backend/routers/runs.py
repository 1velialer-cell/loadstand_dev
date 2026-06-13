from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.repositories.result_repository import (RunResultRepository,)
from backend.repositories.run_repository import (RunRepository,)
from backend.services.run_executor import run_executor
from backend.services.run_service import RunService
from backend.models.schemas import RunCreate

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
    return {
        "id": run.id,
        "tool_name": run.tool_name,
        "status": run.status,
    }

@router.websocket("/{run_id}/ws")
async def run_logs_ws(run_id: str,websocket: WebSocket,):
    await websocket.accept()
    await run_executor.connect(run_id,websocket,)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await run_executor.disconnect(run_id,websocket,)

@router.get("")
async def get_runs(db: Session = Depends(get_db),):
    repo = RunRepository(db)
    return repo.list()

@router.get("/{run_id}")
async def get_run(run_id: str,db: Session = Depends(get_db),):
    repo = RunRepository(db)
    run = repo.get(run_id)
    if not run:
        raise HTTPException(status_code=404,detail="Run not found",)
    return run

@router.get("/{run_id}/result")
async def get_result(run_id: str,db: Session = Depends(get_db),):
    repo = RunResultRepository(db)
    result = repo.get_by_run(run_id)
    if not result:
        raise HTTPException(status_code=404,detail="Result not found",)
    return result