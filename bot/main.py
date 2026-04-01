from fastapi import FastAPI, Request
from flow import handle_message

app = FastAPI()

@app.get("/")
def health():
    return {"status": "KIA Bot activo ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    # Log temporal para ver la estructura completa
    print("WEBHOOK BODY:", body)

    event = body.get("event", "")
    print("EVENT:", event)

    if event not in ("messages.upsert", "MESSAGES_UPSERT"):
        return {"status": "ignored"}

    data = body.get("data", {})
    key = data.get("key", {})

    # Ignorar mensajes propios del bot
    if key.get("fromMe"):
        return {"status": "ignored"}

    message = data.get("message", {})
    phone = key.get("remoteJid", "").replace("@s.whatsapp.net", "")

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text", "")
        or ""
    ).strip()

    print("PHONE:", phone)
    print("TEXT:", text)

    if phone and text:
        await handle_message(phone, text)

    return {"status": "ok"}