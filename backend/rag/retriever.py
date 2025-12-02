from .indexer import get_vectorstore

def retrieve_documents(query: str, k: int = 5):
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return docs
