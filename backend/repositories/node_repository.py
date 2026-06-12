from sqlalchemy.orm import Session
from backend.db.models.node import Node

class NodeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, node):
        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)
        return node

    def get(self, node_id: str):
        return self.db.get(Node, node_id)

    def list(self):
        return self.db.query(Node).all()

    def delete(self, node_id: str):
        node = self.db.get(Node, node_id)
        if not node:
            raise HTTPException(404, "Node not found")
        self.db.delete(node)
        self.db.commit()
        return {"OK": True}

    def update(self, node_id: str, data: dict):
        node = self.db.get(Node, node_id)
        if not node:
            raise HTTPException(404, "Node not found")
        for key, value in data.items():
            setattr(node, key, value)
        self.db.commit()
        self.db.refresh(node)
        return node

    def save(self):
        self.db.commit()