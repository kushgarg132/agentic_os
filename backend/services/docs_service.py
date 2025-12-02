from .auth_utils import get_service
from sqlalchemy.orm import Session

def get_docs_service(user_id: int, db: Session):
    return get_service(user_id, "docs", "v1", db)

def create_doc(user_id: int, db: Session, title: str):
    service = get_docs_service(user_id, db)
    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    return doc.get('documentId')

def get_doc_content(user_id: int, db: Session, document_id: str):
    service = get_docs_service(user_id, db)
    document = service.documents().get(documentId=document_id).execute()
    return document

def append_text(user_id: int, db: Session, document_id: str, text: str):
    service = get_docs_service(user_id, db)
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result
