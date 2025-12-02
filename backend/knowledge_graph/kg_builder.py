from sqlalchemy.orm import Session
from db.models import KGNode, KGEdge
import json

def add_node(db: Session, label: str, name: str, properties: dict = None):
    # Check if exists
    node = db.query(KGNode).filter(KGNode.label == label, KGNode.name == name).first()
    if not node:
        node = KGNode(label=label, name=name, properties=properties)
        db.add(node)
        db.commit()
        db.refresh(node)
    return node

def add_edge(db: Session, source_id: int, target_id: int, relation_type: str, properties: dict = None):
    edge = db.query(KGEdge).filter(
        KGEdge.source_id == source_id,
        KGEdge.target_id == target_id,
        KGEdge.relation_type == relation_type
    ).first()
    
    if not edge:
        edge = KGEdge(source_id=source_id, target_id=target_id, relation_type=relation_type, properties=properties)
        db.add(edge)
        db.commit()
        db.refresh(edge)
    return edge

def build_graph_from_text(db: Session, text: str):
    # TODO: Use LLM to extract entities and relationships
    # This is a placeholder for the actual LLM extraction logic
    pass
