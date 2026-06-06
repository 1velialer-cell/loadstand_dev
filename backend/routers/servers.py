import json
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from backend.core.sec import get_current_user
from backend.models.schemas import (
    ServerCreate,
    ServerDelete,
    ServerPatch,
)

router = APIRouter(
    prefix="/server",
    tags=["server"]
)

DATA_FILE = Path("data/servers.json")

def read_servers():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_servers(servers):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            servers,
            f,
            indent=2,
            ensure_ascii=False
        )

@router.post("")
async def create_server(
    payload: ServerCreate
):
    servers = read_servers()

    server = {
        "id": str(uuid4()),
        **payload.model_dump()
    }

    servers.append(server)

    write_servers(servers)

    return server

@router.get("/media")
async def get_media_servers():

    return [
        server
        for server in read_servers()
        if server["type"] == "media"
    ]

@router.get("/load")
async def get_load_servers():

    return [
        server
        for server in read_servers()
        if server["type"] == "load"
    ]

@router.get("")
async def get_server(
    id: str
):
    for server in read_servers():

        if server["id"] == id:
            return server

    raise HTTPException(
        status_code=404,
        detail="Server not found"
    )

@router.patch("")
async def patch_server(
    payload: ServerPatch
):
    servers = read_servers()
    for server in servers:
        if server["id"] == payload.id:
            updates = payload.model_dump(
                exclude_none=True
            )
            updates.pop("id", None)
            for key, value in updates.items():
                server[key] = value
            write_servers(servers)
            return server
    raise HTTPException(
        status_code=404,
        detail="Server not found"
    )

@router.delete("")
async def delete_server(
    payload: ServerDelete
):
    servers = read_servers()
    filtered = [
        server
        for server in servers
        if server["id"] != payload.id
    ]
    write_servers(filtered)
    return {"status": "OK"}

@router.put("")
async def update_server(
    payload: ServerPatch,
    user: str = Depends(get_current_user)
):
    servers = load_servers()
    for idx, server in enumerate(servers):
        if server["id"] == payload.id:
            servers[idx] = payload.model_dump()
            save_servers(servers)
            return servers[idx]
    raise HTTPException(
        status_code=404,
        detail="Server not found"
    )








