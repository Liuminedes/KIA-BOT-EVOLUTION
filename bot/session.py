import redis.asyncio as redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TTL = 60 * 60

def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)

async def get_session(phone: str) -> dict:
    try:
        r = get_redis()
        data = await r.get(f"session:{phone}")
        await r.aclose()
        return json.loads(data) if data else {"step": "start", "data": {}}
    except Exception as e:
        print(f"Redis error get_session: {e}")
        return {"step": "start", "data": {}}

async def save_session(phone: str, session: dict):
    try:
        r = get_redis()
        await r.set(f"session:{phone}", json.dumps(session), ex=TTL)
        await r.aclose()
    except Exception as e:
        print(f"Redis error save_session: {e}")

async def clear_session(phone: str):
    try:
        r = get_redis()
        await r.delete(f"session:{phone}")
        await r.aclose()
    except Exception as e:
        print(f"Redis error clear_session: {e}")