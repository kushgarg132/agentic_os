from knowledge_graph.kg_builder import add_node, add_edge
from knowledge_graph.kg_queries import search_nodes, get_related_nodes
from db.database import SessionLocal

def save_structured_memory(label: str, name: str, properties: dict = None):
    db = SessionLocal()
    try:
        return add_node(db, label, name, properties)
    finally:
        db.close()

def query_structured_memory(query: str):
    db = SessionLocal()
    try:
        return search_nodes(db, query)
    finally:
        db.close()
