import httpx
import os

BASE_URL = os.getenv("EVOLUTION_URL")
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "kia-bot")

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

async def resolve_lid_to_number(lid: str) -> str:
    """Convierte un LID interno al número real de WhatsApp"""
    try:
        # El LID viene como '186874496860292@lid', lo limpiamos
        lid_clean = lid.replace("@lid", "").replace("@s.whatsapp.net", "")
        url = f"{BASE_URL}/chat/whatsappNumbers/{INSTANCE}"
        payload = {"numbers": [lid_clean]}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(url, json=payload, headers=HEADERS)
            data = r.json()
            # Retorna el número real si existe
            if isinstance(data, list) and data:
                return data[0].get("jid", "").split("@")[0]
    except Exception as e:
        print(f"Error resolviendo LID: {e}")
    return lid_clean

async def send_text(to: str, text: str):
    # Si el número termina en @lid, resolverlo primero
    if "@lid" in to or (not to.startswith("57") and len(to) > 13):
        to = await resolve_lid_to_number(to)

    url = f"{BASE_URL}/message/sendText/{INSTANCE}"
    payload = {
        "number": to,
        "textMessage": {"text": text}
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload, headers=HEADERS)
        print("SEND RESPONSE:", r.status_code, r.text)
        return r.json()

async def send_lead_to_bryan(bryan: str, lead: dict):
    texto = (
        f"🔔 *Nuevo Lead KIA*\n\n"
        f"👤 *Nombre:* {lead.get('nombre')}\n"
        f"📱 *Número:* {lead.get('phone')}\n"
        f"🚗 *Interés:* {lead.get('interes')}\n"
        f"💰 *Presupuesto:* {lead.get('presupuesto')}\n"
        f"📋 *Comentario:* {lead.get('comentario', 'Sin comentarios')}\n"
    )
    await send_text(bryan, texto)