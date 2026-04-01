import redis.asyncio as redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
TTL = 60 * 60 * 2

def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)

async def get_session(phone: str) -> dict:
    try:
        r = get_redis()
        data = await r.get(f"session:{phone}")
        await r.aclose()
        if data:
            print(f"[SESSION] GET {phone} → step: {json.loads(data).get('step')}")
            return json.loads(data)
        print(f"[SESSION] NEW {phone}")
        return {"step": "start", "data": {}}
    except Exception as e:
        print(f"[SESSION ERROR] get: {e}")
        return {"step": "start", "data": {}}

async def save_session(phone: str, session: dict):
    try:
        r = get_redis()
        await r.set(f"session:{phone}", json.dumps(session), ex=TTL)
        await r.aclose()
        print(f"[SESSION] SAVE {phone} → step: {session.get('step')}")
    except Exception as e:
        print(f"[SESSION ERROR] save: {e}")

async def clear_session(phone: str):
    try:
        r = get_redis()
        await r.delete(f"session:{phone}")
        await r.aclose()
        print(f"[SESSION] CLEAR {phone}")
    except Exception as e:
        print(f"[SESSION ERROR] clear: {e}")

async def save_lid_mapping(lid: str, real_jid: str):
    try:
        r = get_redis()
        await r.set(f"lid:{lid}", real_jid, ex=60 * 60 * 24 * 30)
        await r.aclose()
        print(f"[LID] MAPPED {lid} → {real_jid}")
    except Exception as e:
        print(f"[LID ERROR] save: {e}")

async def get_phone_from_lid(lid: str):
    try:
        r = get_redis()
        result = await r.get(f"lid:{lid}")
        await r.aclose()
        print(f"[LID] LOOKUP {lid} → {result}")
        return result
    except Exception as e:
        print(f"[LID ERROR] get: {e}")
        return None