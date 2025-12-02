from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.database import get_db
from auth.oauth import get_authorization_url, fetch_token
from auth.token_store import save_token
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/login")
def login():
    authorization_url, state = get_authorization_url()
    # Store state in session (simplified)
    return RedirectResponse(authorization_url)

@router.get("/callback")
def callback(request: Request, code: str, state: str, db: Session = Depends(get_db)):
    try:
        token_data = fetch_token(code, state)
        # Identify user from id_token (simplified, assume user_id=1 for single user mode)
        user_id = 1 
        save_token(db, user_id, token_data)
        return {"message": "Successfully authenticated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
