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

    # Usar el remoteJid completo — puede ser @lid o @s.whatsapp.net
    phone = key.get("remoteJid", "")

    # Ignorar grupos
    if "@g.us" in phone:
        return {"status": "ignored"}

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text", "")
        or ""
    ).strip()

    print("PHONE RAW:", phone)
    print("TEXT:", text)

    if phone and text:
        await handle_message(phone, text)

    return {"status": "ok"}