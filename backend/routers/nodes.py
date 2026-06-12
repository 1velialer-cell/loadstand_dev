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

@router.post("/{node_id}/check")
async def check_node(node_id: str,service: NodeService = Depends(get_service)):
    return service.check(node_id)