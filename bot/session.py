import redis.asyncio as redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TTL = 60 * 60 * 2  # 2 horas

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

async def save_lid_mapping(lid: str, real_jid: str):
    try:
        r = get_redis()
        await r.set(f"lid:{lid}", real_jid, ex=60 * 60 * 24 * 30)
        print(f"LID mapeado: {lid} → {real_jid}")
        await r.aclose()
    except Exception as e:
        print(f"Redis error save_lid_mapping: {e}")

async def get_phone_from_lid(lid: str) -> str:
    try:
        r = get_redis()
        result = await r.get(f"lid:{lid}")
        await r.aclose()
        return result if result else None
    except Exception as e:
        print(f"Redis error get_phone_from_lid: {e}")
        return None