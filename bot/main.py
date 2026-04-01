from fastapi import FastAPI, Request
from flow import handle_message

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

    message = data.get("message", {})

    # En v1.8.2 el número del cliente está en data.sender
    sender = data.get("sender", "")
    phone = sender.split("@")[0] if sender else key.get("remoteJid", "").split("@")[0]

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text", "")
        or ""
    ).strip()

    print("PHONE FINAL:", phone)
    print("TEXT:", text)

    if phone and text:
        await handle_message(phone, text)

    return {"status": "ok"}