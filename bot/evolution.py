import httpx
import os

BASE_URL = os.getenv("EVOLUTION_URL")
API_KEY  = os.getenv("EVOLUTION_API_KEY")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "kia-bot")

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

async def send_text(to: str, text: str):
    url = f"{BASE_URL}/message/sendText/{INSTANCE}"
    # Enviar JID completo — @lid, @s.whatsapp.net, o número limpio
    payload = {
        "number": to,
        "textMessage": {"text": text}
    }
    print(f"[EVOLUTION] SENDING → {to}")
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, json=payload, headers=HEADERS)
        print(f"[EVOLUTION] RESPONSE → {r.status_code} | {r.text[:200]}")
        return r.json()

async def send_lead_to_bryan(bryan: str, lead: dict):
    print(f"[EVOLUTION] LEAD → Bryan: {bryan}")
    texto = (
        f"🔔 *Nuevo Lead KIA*\n\n"
        f"👤 *Nombre:* {lead.get('nombre')}\n"
        f"📱 *Contacto:* {lead.get('pushName', lead.get('phone_display', ''))}\n"
        f"🚗 *Interés:* {lead.get('interes')}\n"
        f"💰 *Presupuesto:* {lead.get('presupuesto')}\n"
        f"💼 *Tipo de compra:* {lead.get('tipo_compra', 'No especificado')}\n"
        f"📋 *Comentario:* {lead.get('comentario', 'Sin comentarios')}\n"
    )
    await send_text(bryan, texto)