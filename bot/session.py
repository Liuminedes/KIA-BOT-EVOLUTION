import redis.asyncio as redis
import json
from config import REDIS_URL

r = redis.from_url(REDIS_URL, decode_responses=True)
TTL = 60 * 60  # 1 hora de sesión activa

async def get_session(phone: str) -> dict:
    data = await r.get(f"session:{phone}")
    return json.loads(data) if data else {"step": "start", "data": {}}

async def save_session(phone: str, session: dict):
    await r.set(f"session:{phone}", json.dumps(session), ex=TTL)

async def clear_session(phone: str):
    await r.delete(f"session:{phone}")