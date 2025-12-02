from .auth_utils import get_service
from sqlalchemy.orm import Session
from googleapiclient.http import MediaIoBaseDownload
import io

def get_drive_service(user_id: int, db: Session):
    return get_service(user_id, "drive", "v3", db)

def search_files(user_id: int, db: Session, query: str, page_size: int = 10):
    service = get_drive_service(user_id, db)
    results = service.files().list(
        q=query, pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    return results.get('files', [])

def download_file(user_id: int, db: Session, file_id: str):
    service = get_drive_service(user_id, db)
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return fh.getvalue()

def get_file_metadata(user_id: int, db: Session, file_id: str):
    service = get_drive_service(user_id, db)
    return service.files().get(fileId=file_id).execute()
