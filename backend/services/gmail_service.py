from .auth_utils import get_service
from sqlalchemy.orm import Session
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def get_gmail_service(user_id: int, db: Session):
    return get_service(user_id, "gmail", "v1", db)

def list_messages(user_id: int, db: Session, query: str = None, max_results: int = 10):
    service = get_gmail_service(user_id, db)
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    return results.get('messages', [])

def get_message(user_id: int, db: Session, msg_id: str):
    service = get_gmail_service(user_id, db)
    return service.users().messages().get(userId='me', id=msg_id).execute()

def create_message(sender: str, to: str, subject: str, message_text: str, file_attachment: dict = None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    if file_attachment:
        # file_attachment expected to have 'filename' and 'content' (bytes)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_attachment['content'])
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{file_attachment["filename"]}"'
        )
        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(user_id: int, db: Session, to: str, subject: str, body: str, attachment: dict = None):
    service = get_gmail_service(user_id, db)
    # Get user profile to find sender email
    profile = service.users().getProfile(userId='me').execute()
    sender = profile['emailAddress']
    
    message = create_message(sender, to, subject, body, attachment)
    return service.users().messages().send(userId='me', body=message).execute()
