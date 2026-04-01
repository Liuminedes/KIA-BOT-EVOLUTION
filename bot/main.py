from fastapi import FastAPI, Request
from flow import handle_message
import os

app = FastAPI()

BRYAN_NUMBER = os.getenv("BRYAN_NUMBER", "573007271627")

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

    # Ignorar mensajes enviados por el bot
    if key.get("fromMe"):
        return {"status": "ignored"}

    message = data.get("message", {})

    # El número del cliente viene en key.remoteJid cuando fromMe es false
    # y el mensaje viene de afuera hacia Bryan
    remote_jid = key.get("remoteJid", "")
    phone = remote_jid.split("@")[0]

    # Ignorar si es el propio número de Bryan
    if phone == BRYAN_NUMBER or phone == BRYAN_NUMBER.replace("57", "", 1):
        return {"status": "ignored"}

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