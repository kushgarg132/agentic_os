from sqlalchemy.orm import Session
from db.models import KGNode, KGEdge

def search_nodes(db: Session, query: str):
    return db.query(KGNode).filter(KGNode.name.ilike(f"%{query}%")).all()

def get_related_nodes(db: Session, node_id: int):
    edges = db.query(KGEdge).filter(KGEdge.source_id == node_id).all()
    related = []
    for edge in edges:
        target = db.query(KGNode).filter(KGNode.id == edge.target_id).first()
        if target:
            related.append({"relation": edge.relation_type, "node": target})
    return related
