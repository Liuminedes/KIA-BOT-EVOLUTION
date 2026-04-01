from session import get_session, save_session, clear_session
from evolution import send_text, send_lead_to_bryan
from config import BRYAN_NUMBER

MESSAGES = {
    "start": (
        "👋 ¡Hola! Bienvenido al asistente virtual de *KIA Colombia* 🚗\n\n"
        "Soy el asistente de *Bryan Losada*, asesor KIA certificado.\n\n"
        "Estoy aquí para ayudarte a encontrar el vehículo ideal. "
        "¿Con quién tengo el gusto de hablar?"
    ),
    "nombre": (
        "¡Mucho gusto, *{nombre}*! 😊\n\n"
        "¿Qué modelo KIA te llama la atención?\n\n"
        "1️⃣ KIA Sportage — SUV familiar, desde $119M\n"
        "2️⃣ KIA Picanto — Compacto urbano, desde $62M\n"
        "3️⃣ KIA Sonet — SUV compacto, desde $89M\n"
        "4️⃣ KIA Stinger — Sedán deportivo, desde $189M\n"
        "5️⃣ KIA EV6 — 100% eléctrico, desde $189M\n"
        "6️⃣ Aún no lo tengo claro, necesito asesoría"
    ),
    "interes": (
        "Excelente elección 🙌\n\n"
        "¿Cuál es tu presupuesto aproximado?\n\n"
        "1️⃣ Hasta $80 millones\n"
        "2️⃣ Entre $80M y $120M\n"
        "3️⃣ Entre $120M y $180M\n"
        "4️⃣ Más de $180 millones"
    ),
    "presupuesto": (
        "Perfecto 👍\n\n"
        "¿Cómo planeas realizar la compra?\n\n"
        "1️⃣ Contado\n"
        "2️⃣ Crédito bancario\n"
        "3️⃣ Leasing\n"
        "4️⃣ Aún no lo decido"
    ),
    "tipo_compra": (
        "Entendido ✅\n\n"
        "¿Tienes alguna pregunta adicional para Bryan o algo "
        "específico que quieras saber sobre el vehículo?\n\n"
        "_(Escribe tu duda o escribe *no* para continuar)_"
    ),
    "done": (
        "✅ ¡Listo, *{nombre}*!\n\n"
        "Tu información fue enviada a *Bryan Losada* quien te "
        "contactará muy pronto para brindarte una atención "
        "personalizada. 🤝\n\n"
        "¡Gracias por tu interés en *KIA*! 🚗💨"
    ),
}

INTEREST_MAP = {
    "1": "KIA Sportage",
    "2": "KIA Picanto",
    "3": "KIA Sonet",
    "4": "KIA Stinger",
    "5": "KIA EV6",
    "6": "Necesita asesoría — sin modelo definido",
}

BUDGET_MAP = {
    "1": "Hasta $80M",
    "2": "Entre $80M y $120M",
    "3": "Entre $120M y $180M",
    "4": "Más de $180M",
}

PURCHASE_MAP = {
    "1": "Contado",
    "2": "Crédito bancario",
    "3": "Leasing",
    "4": "Por decidir",
}

async def handle_message(phone: str, text: str, push_name: str = ""):
    text = text.strip()
    session = await get_session(phone)
    step = session.get("step", "start")
    data = session.get("data", {})

    print(f"[FLOW] phone={phone} step={step} text={text[:30]} pushName={push_name}")

    phone_display = phone.replace("@lid", "").replace("@s.whatsapp.net", "")

    if step == "start":
        await send_text(phone, MESSAGES["start"])
        await save_session(phone, {
            "step": "nombre",
            "data": {
                "phone": phone,
                "phone_display": phone_display,
                "pushName": push_name
            }
        })

    elif step == "nombre":
        if len(text) < 2 or text.isdigit():
            await send_text(phone, "Por favor escribe tu nombre completo 😊")
            return
        data["nombre"] = text.title()
        msg = MESSAGES["nombre"].format(nombre=data["nombre"])
        await send_text(phone, msg)
        await save_session(phone, {"step": "interes", "data": data})

    elif step == "interes":
        data["interes"] = INTEREST_MAP.get(text, text)
        await send_text(phone, MESSAGES["interes"])
        await save_session(phone, {"step": "presupuesto", "data": data})

    elif step == "presupuesto":
        data["presupuesto"] = BUDGET_MAP.get(text, text)
        await send_text(phone, MESSAGES["presupuesto"])
        await save_session(phone, {"step": "tipo_compra", "data": data})

    elif step == "tipo_compra":
        data["tipo_compra"] = PURCHASE_MAP.get(text, text)
        await send_text(phone, MESSAGES["tipo_compra"])
        await save_session(phone, {"step": "comentario", "data": data})

    elif step == "comentario":
        data["comentario"] = text if text.lower() not in ("no", "ninguna", "nada") else "Sin comentarios"
        await send_lead_to_bryan(BRYAN_NUMBER, data)
        msg = MESSAGES["done"].format(nombre=data.get("nombre", ""))
        await send_text(phone, msg)
        await clear_session(phone)