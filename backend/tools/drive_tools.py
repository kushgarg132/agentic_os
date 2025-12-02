from langchain.tools import tool
from services.drive_service import search_files, get_file_metadata
from db.database import SessionLocal

@tool
def search_drive_files(user_id: int, query: str):
    """Searches for files in Google Drive."""
    db = SessionLocal()
    try:
        return search_files(user_id, db, query)
    finally:
        db.close()
