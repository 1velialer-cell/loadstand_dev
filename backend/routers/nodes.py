from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.repositories.node_repository import NodeRepository
from backend.services.node_service import NodeService
from backend.models.schemas import NodeCreate, NodeUpdate
from backend.db.models.enums import NodeStatus

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
async def delete_node(node_id: str, service: NodeService = Depends(get_service)):
    return await service.delete(node_id)

@router.patch("/{node_id}")
async def update_node(node_id: str, payload: NodeUpdate, service: NodeService = Depends(get_service)):
    return await service.update(node_id, payload.model_dump(exclude_unset=True))

from backend.services.ssh_executor import executor
from datetime import datetime

@router.post("/{node_id}/check")
async def check_node(node_id: str, db: Session = Depends(get_db)):
    repo = NodeRepository(db)
    node = repo.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    status = NodeStatus.OFFLINE
    last_seen = None
    error = None
    try:
        await executor.get_connection(node)
        status = NodeStatus.ONLINE
        last_seen = datetime.utcnow()
    except Exception as exc:
        error = str(exc)
    repo.update(node_id, {"status": status, "last_seen": last_seen} if last_seen else {"status": status})
    return {"status": status.value, "last_seen": last_seen.isoformat() if last_seen else None, "error": error}

@router.post("/check-all")
async def check_all_nodes(db: Session = Depends(get_db)):
    repo = NodeRepository(db)
    nodes = repo.list()
    results = []
    for node in nodes:
        status = NodeStatus.OFFLINE
        last_seen = None
        error = None
        try:
            await executor.get_connection(node)
            status = NodeStatus.ONLINE
            last_seen = datetime.utcnow()
            repo.update(node.id, {"status": status, "last_seen": last_seen})
        except Exception as exc:
            error = str(exc)
            repo.update(node.id, {"status": status})
        results.append({
            "node_id": node.id,
            "name": node.name,
            "status": status.value,
            "last_seen": last_seen.isoformat() if last_seen else None,
            "error": error,
        })
    return results