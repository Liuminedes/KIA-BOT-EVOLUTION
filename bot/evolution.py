import httpx
from config import EVOLUTION_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

HEADERS = {
    "apikey": EVOLUTION_API_KEY,
    "Content-Type": "application/json"
}

async def send_text(to: str, text: str):
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    payload = {"number": to, "text": text}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json=payload, headers=HEADERS)
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