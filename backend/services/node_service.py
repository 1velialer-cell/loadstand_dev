from datetime import datetime
import socket
from backend.db.models.node import Node, NodeStatus
from backend.services.ssh_executor import executor
from typing import Optional

class NodeService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, data: dict):
        node = Node(**data)
        if not node.status:
            node.status = NodeStatus.UNKNOWN
        return self.repo.create(node)

    def list(self):
        return self.repo.list()

    def get(self, node_id: str):
        return self.repo.get(node_id)

    async def delete(self, node_id: str):
        await executor.invalidate_connection(node_id)
        return self.repo.delete(node_id)

    async def update(self, node_id: str, data: dict):
        if any(key in data for key in ("host", "port", "ssh_login", "ssh_password")):
            await executor.invalidate_connection(node_id)
        return self.repo.update(node_id, data)

    def check(self, node_id: str):
        node = self.repo.get(node_id)
        if not node:
            raise ValueError("Node not found")

        host = getattr(node, "host", None)
        port = getattr(node, "port", None)
        is_online = False
        last_seen: Optional[datetime] = None
        try:
            if host and port:
                conn = socket.create_connection((host, port), timeout=3)
                conn.close()
                is_online = True
                last_seen = datetime.utcnow()
        except Exception:
            is_online = False

        status = NodeStatus.ONLINE if is_online else NodeStatus.OFFLINE
        data = {"status": status}
        if last_seen:
            data["last_seen"] = last_seen

        # persist changes
        updated = self.repo.update(node_id, data)
        return {"status": status.value, "last_seen": last_seen.isoformat() if last_seen else None}