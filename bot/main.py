from fastapi import FastAPI, Request
from flow import handle_message
from session import save_lid_mapping, get_phone_from_lid
import os
import json

app = FastAPI()
BRYAN_NUMBER = os.getenv("BRYAN_NUMBER", "573007271627")

@app.get("/")
def health():
    return {"status": "KIA Bot activo ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    event = body.get("event", "")

    print(f"[WEBHOOK] event={event}")

    # Capturar LID desde contacts.update
    if event in ("CONTACTS_UPDATE", "contacts.update"):
        data = body.get("data", [])
        items = data if isinstance(data, list) else [data]
        for contact in items:
            lid = contact.get("id", "")
            push_name = contact.get("pushName", "")
            if "@lid" in lid:
                print(f"[CONTACTS] LID detectado: {lid} | pushName: {push_name}")
                # No tenemos el número real en v1.8.2 — guardamos el pushName
                await save_lid_mapping(lid, lid)  # guardamos el lid mismo como fallback
        return {"status": "ok"}

    if event not in ("messages.upsert", "MESSAGES_UPSERT"):
        return {"status": "ignored"}

    data = body.get("data", {})
    key = data.get("key", {})

    if key.get("fromMe"):
        print("[WEBHOOK] ignored: fromMe=true")
        return {"status": "ignored"}

    message = data.get("message", {})
    raw_jid = key.get("remoteJid", "")
    push_name = data.get("pushName", "")

    print(f"[WEBHOOK] raw_jid={raw_jid} pushName={push_name}")

    if "@g.us" in raw_jid:
        return {"status": "ignored"}

    # Usar el JID completo directamente — @lid o @s.whatsapp.net
    phone = raw_jid

    # Ignorar mensajes del número de Bryan
    phone_clean = raw_jid.split("@")[0]
    if phone_clean == BRYAN_NUMBER:
        print(f"[WEBHOOK] ignored: mensaje del número de Bryan")
        return {"status": "ignored"}

    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text", "")
        or ""
    ).strip()

    print(f"[WEBHOOK] PROCESANDO phone={phone} text={text[:50]}")

    if phone and text:
        await handle_message(phone, text, push_name)

    return {"status": "ok"}