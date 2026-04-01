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

    # Parsear el número correctamente
    remote_jid = key.get("remoteJid", "")
    phone = remote_jid.split("@")[0]

    # Si el número no empieza con 57, puede ser un JID interno
    # usamos el campo sender como fallback
    if not phone.startswith("57"):
        sender = body.get("sender", "") or data.get("sender", "")
        phone = sender.split("@")[0] if sender else phone

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