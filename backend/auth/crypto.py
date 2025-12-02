from cryptography.fernet import Fernet
import base64
from config import settings

# Ensure ENCRYPTION_KEY is valid base64
try:
    key = base64.urlsafe_b64decode(settings.ENCRYPTION_KEY)
    if len(key) != 32:
        raise ValueError("ENCRYPTION_KEY must be 32 bytes")
    fernet = Fernet(settings.ENCRYPTION_KEY)
except Exception as e:
    print(f"Warning: Encryption key issue: {e}. Token encryption will fail if not fixed.")
    # Fallback for build/test if key is missing, but should be set in prod
    fernet = None

def encrypt_token(token: str) -> str:
    if not fernet:
        raise ValueError("Encryption key not configured")
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    if not fernet:
        raise ValueError("Encryption key not configured")
    return fernet.decrypt(encrypted_token.encode()).decode()
