from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.db.models.node import Node
from backend.repositories.node_repository import NodeRepository
from backend.services.ssh_executor import executor

router = APIRouter(prefix="/ssh", tags=["ssh"])

async def get_node(node_id: str, db: Session = Depends(get_db)) -> Node:
    repo = NodeRepository(db)
    node = repo.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

from backend.models.schemas import SSHCommandRequest

@router.post("/{node_id}/execute")
async def execute_command(node_id: str, payload: SSHCommandRequest, node: Node = Depends(get_node)):
    command = payload.command
    if not command:
        raise HTTPException(status_code=400, detail="command is required")
    try:
        return await executor.execute_command(node, command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/{node_id}/reset")
async def reset_connection(node_id: str, node: Node = Depends(get_node)):
    try:
        await executor.invalidate_connection(node_id)
        return {"status": "reset"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/{node_id}/status")
async def ssh_status(node_id: str, node: Node = Depends(get_node)):
    try:
        await executor.get_connection(node)
        return {"status": "ONLINE"}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/commands/{command_id}/stop")
async def stop_command(command_id: str):
    try:
        return await executor.stop_command(command_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="command not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/commands/{command_id}")
async def get_command(command_id: str):
    try:
        return executor.get_command(command_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="command not found")
