from langchain.tools import tool
from sqlalchemy.orm import Session
from services.drive_service import search_files, download_file
from services.gmail_service import send_email
from db.database import SessionLocal
import base64

@tool
def send_drive_file_via_email(filename: str, recipient: str, user_id: int):
    """
    Searches for a file in Google Drive by name, downloads it, and sends it to the specified recipient via Gmail.
    """
    db: Session = SessionLocal()
    try:
        # 1. Search for file
        files = search_files(user_id, db, query=f"name contains '{filename}'")
        if not files:
            return f"Error: No file found matching '{filename}'."
        
        if len(files) > 1:
            # For now, pick the first one, but ideally ask for clarification
            # In a real agent loop, we'd return a list and ask the user to clarify
            pass
        
        target_file = files[0]
        file_id = target_file['id']
        file_name = target_file['name']
        
        # 2. Download file
        content = download_file(user_id, db, file_id)
        
        # 3. Send email
        attachment = {
            'filename': file_name,
            'content': content
        }
        
        send_email(
            user_id, 
            db, 
            to=recipient, 
            subject=f"File: {file_name}", 
            body=f"Please find attached the file: {file_name}", 
            attachment=attachment
        )
        
        return f"Successfully sent '{file_name}' to {recipient}."
        
    except Exception as e:
        return f"Failed to send file: {str(e)}"
    finally:
        db.close()
