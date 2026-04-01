from fastapi import FastAPI, Request
from flow import handle_message
from session import save_lid_mapping, get_phone_from_lid
import os

app = FastAPI()
BRYAN_NUMBER = os.getenv("BRYAN_NUMBER", "573007271627")

@app.get("/")
def health():
    return {"status": "KIA Bot activo ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    import json
    print("FULL BODY:", json.dumps(body, indent=2, default=str))
    event = body.get("event", "")

    # Capturar mapeo LID → número real
    if event in ("CONTACTS_UPDATE", "contacts.update"):
        data = body.get("data", [])
        if isinstance(data, list):
            for contact in data:
                lid = contact.get("id", "")
                phone_number = contact.get("phoneNumber", "") or contact.get("number", "")
                if "@lid" in lid and phone_number:
                    clean_phone = phone_number.replace("+", "").replace(" ", "")
                    await save_lid_mapping(lid, f"{clean_phone}@s.whatsapp.net")
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

    # Resolver LID si aplica
    if "@lid" in raw_jid:
        resolved = await get_phone_from_lid(raw_jid)
        phone = resolved if resolved else raw_jid
    else:
        phone = raw_jid

    # Ignorar mensajes del propio número de Bryan
    phone_clean = phone.split("@")[0]
    if phone_clean == BRYAN_NUMBER:
        return {"status": "ignored"}

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text", "")
        or ""
    ).strip()

    if phone and text:
        await handle_message(phone, text)

    return {"status": "ok"}