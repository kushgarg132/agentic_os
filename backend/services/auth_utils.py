from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from auth.token_store import get_token, save_token
from config import settings

def get_credentials(user_id: int, db: Session):
    token_data = get_token(db, user_id)
    if not token_data:
        raise ValueError("User not authenticated")
    
    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=token_data["scope"].split(" ")
    )
    
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update token in DB
        new_token_data = {
            "access_token": creds.token,
            "refresh_token": creds.refresh_token, # Might be same
            "expires_at": creds.expiry,
            "scope": " ".join(creds.scopes)
        }
        save_token(db, user_id, new_token_data)
        
    return creds

def get_service(user_id: int, service_name: str, version: str, db: Session):
    creds = get_credentials(user_id, db)
    return build(service_name, version, credentials=creds)
