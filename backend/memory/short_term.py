from config import settings
import redis

# Simple Redis-based short-term memory (e.g., conversation history)
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

def add_to_short_term(user_id: int, message: str):
    key = f"short_term:{user_id}"
    r.rpush(key, message)
    r.ltrim(key, -10, -1)  # Keep last 10

def get_short_term(user_id: int):
    key = f"short_term:{user_id}"
    return [m.decode() for m in r.lrange(key, 0, -1)]
