from rag.indexer import index_text
from rag.retriever import retrieve_documents

def save_long_term_memory(content: str, metadata: dict):
    index_text(content, metadata)

def query_long_term_memory(query: str):
    return retrieve_documents(query)
