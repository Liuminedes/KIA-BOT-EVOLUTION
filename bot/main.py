from fastapi import FastAPI, Request
from flow import handle_message
from session import save_lid_mapping, get_phone_from_lid
import os

app = FastAPI()

@app.get("/")
def health():
    return {"status": "KIA Bot activo ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    event = body.get("event", "")

    # Capturar mapeo LID → número real desde contactos
    if event == "CONTACTS_UPDATE":
        data = body.get("data", [])
        if isinstance(data, list):
            for contact in data:
                lid = contact.get("id", "")
                phone = contact.get("phoneNumber") or contact.get("number") or contact.get("pushName")
                remapped = contact.get("remoteJid", "")
                if lid and "@lid" in lid:
                    # Buscar el número real en los campos disponibles
                    real_jid = remapped if remapped and "@s.whatsapp.net" in remapped else None
                    if real_jid:
                        await save_lid_mapping(lid, real_jid)
        return {"status": "ok"}

    if event not in ("messages.upsert", "MESSAGES_UPSERT"):
        return {"status": "ignored"}

    data = body.get("data", {})
    key = data.get("key", {})

    if key.get("fromMe"):
        return {"status": "ignored"}

    message = data.get("message", {})
    raw_jid = key.get("remoteJid", "")

    if "@g.us" in raw_jid:
        return {"status": "ignored"}

    # Si es LID, intentar resolver al número real
    if "@lid" in raw_jid:
        resolved = await get_phone_from_lid(raw_jid)
        phone = resolved if resolved else raw_jid
    else:
        phone = raw_jid

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