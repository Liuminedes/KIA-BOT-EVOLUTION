from fastapi import FastAPI, Request
from flow import handle_message
import json

app = FastAPI()

@app.get("/")
def health():
    return {"status": "KIA Bot activo ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    event = body.get("event", "")

    if event not in ("messages.upsert", "MESSAGES_UPSERT"):
        return {"status": "ignored"}

    data = body.get("data", {})
    key = data.get("key", {})

    if key.get("fromMe"):
        return {"status": "ignored"}

    # Log completo para ver todos los campos disponibles
    print("=== KEY ===", json.dumps(key, indent=2))
    print("=== DATA KEYS ===", list(data.keys()))
    print("=== BODY KEYS ===", list(body.keys()))

    return {"status": "ok"}