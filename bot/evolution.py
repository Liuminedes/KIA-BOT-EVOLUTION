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
    # Limpiar el JID — enviar solo el número sin @
    number = to.split("@")[0] if "@" in to else to
    payload = {
        "number": number,
        "textMessage": {"text": text}
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, json=payload, headers=HEADERS)
        print(f"SEND → {number} | {r.status_code}")
        return r.json()

async def send_lead_to_bryan(bryan: str, lead: dict):
    texto = (
        f"🔔 *Nuevo Lead KIA*\n\n"
        f"👤 *Nombre:* {lead.get('nombre')}\n"
        f"📱 *Número:* {lead.get('phone_display', lead.get('phone', ''))}\n"
        f"🚗 *Interés:* {lead.get('interes')}\n"
        f"💰 *Presupuesto:* {lead.get('presupuesto')}\n"
        f"💼 *Tipo de compra:* {lead.get('tipo_compra', 'No especificado')}\n"
        f"📋 *Comentario:* {lead.get('comentario', 'Sin comentarios')}\n"
    )
    await send_text(bryan, texto)