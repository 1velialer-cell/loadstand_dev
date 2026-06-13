from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.repositories.node_repository import NodeRepository
from backend.services.node_service import NodeService
from backend.models.schemas import NodeCreate, NodeUpdate

router = APIRouter(prefix="/nodes", tags=["nodes"])

def get_service(db: Session = Depends(get_db)):
    return NodeService(NodeRepository(db))

@router.post("")
async def create_node(payload: NodeCreate, service: NodeService = Depends(get_service)):
    return service.create(payload.model_dump())

@router.get("")
async def list_nodes(service: NodeService = Depends(get_service)):
    return service.list()

@router.delete("/{node_id}")
async def delete_node(node_id: str,service: NodeService = Depends(get_service)):
    return service.delete(node_id)

@router.patch("/{node_id}")
async def update_node(node_id: str,payload: NodeUpdate,service: NodeService = Depends(get_service)):
    return service.update(node_id, payload.model_dump(exclude_unset=True))

from backend.services.ssh_executor import executor
from datetime import datetime

@router.post("/{node_id}/check")
async def check_node(node_id: str, db: Session = Depends(get_db)):
    repo = NodeRepository(db)
    node = repo.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    try:
        # attempt to establish SSH connection using executor (raises on credentials/error)
        await executor.get_connection(node)
        repo.update(node_id, {"status": "ONLINE", "last_seen": datetime.utcnow()})
        return {"status": "ONLINE"}
    except Exception as exc:
        repo.update(node_id, {"status": "OFFLINE"})
        raise HTTPException(status_code=400, detail=str(exc))