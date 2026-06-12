from datetime import datetime
import socket
from backend.db.models.node import Node, NodeStatus

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

    def delete(self, node_id: str):
        return self.repo.delete(node_id)

    def update(self, node_id: str, data: dict):
        return self.repo.update(node_id, data)

    def check(self, node_id: str):
        return {"status": "ok"}