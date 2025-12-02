from .auth_utils import get_service
from sqlalchemy.orm import Session

def get_people_service(user_id: int, db: Session):
    return get_service(user_id, "people", "v1", db)

def list_contacts(user_id: int, db: Session, page_size: int = 10):
    service = get_people_service(user_id, db)
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=page_size,
        personFields='names,emailAddresses'
    ).execute()
    return results.get('connections', [])
