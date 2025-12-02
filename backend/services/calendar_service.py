from .auth_utils import get_service
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def get_calendar_service(user_id: int, db: Session):
    return get_service(user_id, "calendar", "v3", db)

def list_events(user_id: int, db: Session, max_results: int = 10):
    service = get_calendar_service(user_id, db)
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])

def create_event(user_id: int, db: Session, summary: str, start_time: str, end_time: str, description: str = None):
    service = get_calendar_service(user_id, db)
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event
