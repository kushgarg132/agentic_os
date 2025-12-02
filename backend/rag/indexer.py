from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embeddings import get_embeddings
import os

CHROMADB_DIR = "./chroma_db"

def get_vectorstore():
    embeddings = get_embeddings()
    return Chroma(persist_directory=CHROMADB_DIR, embedding_function=embeddings)

def index_text(text: str, metadata: dict):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    
    metadatas = [metadata for _ in texts]
    
    vectorstore = get_vectorstore()
    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    vectorstore.persist()

def index_document(file_path: str, metadata: dict):
    # Load document based on extension (simplified)
    with open(file_path, 'r') as f:
        text = f.read()
    index_text(text, metadata)
