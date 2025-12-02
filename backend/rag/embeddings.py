from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from config import settings

def get_embeddings():
    if settings.OPENAI_API_KEY:
        return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
