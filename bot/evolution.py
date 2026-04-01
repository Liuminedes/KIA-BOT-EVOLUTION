import httpx
import os

BASE_URL = os.getenv("EVOLUTION_URL")
API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "kia-bot")

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

async def send_text(to: str, text: str):
    url = f"{BASE_URL}/message/sendText/{INSTANCE}"
    payload = {
        "number": to,  # JID completo: puede ser @lid, @s.whatsapp.net, o número limpio
        "textMessage": {"text": text}
    }
    async with httpx.AsyncClient(timeout=15) as client:
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