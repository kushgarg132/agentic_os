from google_auth_oauthlib.flow import Flow
from config import settings
import os

# Scopes required by the system
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/contacts.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

def get_google_flow(state=None):
    """
    Creates a Google OAuth Flow instance.
    """
    # Ensure client_secrets.json exists or load from env
    # For now, we assume client_secrets.json is in the root or config
    # Better to construct from env vars if possible, but Flow.from_client_config is safer
    
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
        }
    }
    
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    return flow

def get_authorization_url():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return authorization_url, state

def fetch_token(code: str, state: str):
    flow = get_google_flow(state=state)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_at": credentials.expiry,
        "scope": " ".join(credentials.scopes) if credentials.scopes else "",
        "token_type": "Bearer",
        "id_token": credentials.id_token
    }
