from langchain.tools import tool
from services.calendar_service import list_events, create_event
from db.database import SessionLocal

@tool
def list_events_tool(user_id: int, count: int = 10):
    """Lists upcoming events from the user's primary calendar."""
    db = SessionLocal()
    try:
        return list_events(user_id, db, max_results=count)
    finally:
        db.close()

@tool
def create_event_tool(user_id: int, summary: str, start_time: str, end_time: str, description: str = None):
    """Creates a new event in the user's primary calendar.
    start_time and end_time should be in ISO format (e.g., '2023-10-27T10:00:00Z').
    """
    db = SessionLocal()
    try:
        return create_event(user_id, db, summary, start_time, end_time, description)
    finally:
        db.close()
