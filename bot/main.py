from fastapi import FastAPI, Request
from flow import handle_message
import os

app = FastAPI()

BRYAN_NUMBER = os.getenv("BRYAN_NUMBER", "").replace("+", "")

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

    # Ignorar mensajes propios
    if key.get("fromMe"):
        return {"status": "ignored"}

    message = data.get("message", {})
    sender = body.get("sender", "")
    phone = sender.split("@")[0]

    # Ignorar si el sender es el número de Bryan (el vinculado)
    if phone == BRYAN_NUMBER or phone == BRYAN_NUMBER.lstrip("57"):
        print("IGNORADO: mensaje del número vinculado")
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