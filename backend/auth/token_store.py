from sqlalchemy.orm import Session
from db.models import OAuthToken
from .crypto import encrypt_token, decrypt_token
import json
from datetime import datetime

def save_token(db: Session, user_id: int, token_data: dict, service: str = "google"):
    """
    Save or update OAuth token for a user.
    token_data expected to have: access_token, refresh_token, expires_at, scope
    """
    # Encrypt tokens
    encrypted_access = encrypt_token(token_data["access_token"])
    encrypted_refresh = encrypt_token(token_data.get("refresh_token", "")) if token_data.get("refresh_token") else None
    
    # Check if token exists
    db_token = db.query(OAuthToken).filter(OAuthToken.user_id == user_id, OAuthToken.service == service).first()
    
    if db_token:
        db_token.access_token = encrypted_access
        if encrypted_refresh:
            db_token.refresh_token = encrypted_refresh
        db_token.expires_at = token_data.get("expires_at")
        db_token.scopes = json.dumps(token_data.get("scope", "").split(" "))
    else:
        db_token = OAuthToken(
            user_id=user_id,
            service=service,
            access_token=encrypted_access,
            refresh_token=encrypted_refresh,
            expires_at=token_data.get("expires_at"),
            scopes=json.dumps(token_data.get("scope", "").split(" "))
        )
        db.add(db_token)
    
    db.commit()
    db.refresh(db_token)
    return db_token

def get_token(db: Session, user_id: int, service: str = "google") -> dict:
    """
    Retrieve and decrypt OAuth token for a user.
    """
    db_token = db.query(OAuthToken).filter(OAuthToken.user_id == user_id, OAuthToken.service == service).first()
    
    if not db_token:
        return None
        
    return {
        "access_token": decrypt_token(db_token.access_token),
        "refresh_token": decrypt_token(db_token.refresh_token) if db_token.refresh_token else None,
        "expires_at": db_token.expires_at,
        "scope": " ".join(json.loads(db_token.scopes)) if db_token.scopes else "",
        "token_type": db_token.token_type
    }
