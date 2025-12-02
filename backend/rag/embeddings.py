from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

def get_embeddings():
    if settings.GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
