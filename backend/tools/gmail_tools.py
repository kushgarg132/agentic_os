from langchain.tools import tool
from services.gmail_service import list_messages, send_email, create_message
from db.database import SessionLocal

@tool
def read_recent_emails(user_id: int, count: int = 5):
    """Reads the most recent emails from the user's inbox."""
    db = SessionLocal()
    try:
        messages = list_messages(user_id, db, max_results=count)
        # Fetch details for each (simplified)
        return messages
    finally:
        db.close()

@tool
def send_email_tool(user_id: int, to: str, subject: str, body: str):
    """Sends an email to the specified recipient."""
    db = SessionLocal()
    try:
        return send_email(user_id, db, to, subject, body)
    finally:
        db.close()
