from session import get_session, save_session, clear_session
from evolution import send_text, send_lead_to_bryan
from config import BRYAN_NUMBER

STEPS = {
    "start":        "nombre",
    "nombre":       "interes",
    "interes":      "presupuesto",
    "presupuesto":  "comentario",
    "comentario":   "done",
}

MESSAGES = {
    "start": (
        "👋 ¡Hola! Bienvenido a *KIA Colombia* con el asesor Bryan Losada.\n\n"
        "Estoy aquí para ayudarte a encontrar tu próximo vehículo. 🚗\n\n"
        "¿Cuál es tu nombre?"
    ),
    "nombre": (
        "Mucho gusto, {nombre}! 😊\n\n"
        "¿Qué modelo KIA te interesa?\n\n"
        "1️⃣ KIA Sportage\n"
        "2️⃣ KIA Picanto\n"
        "3️⃣ KIA Sonet\n"
        "4️⃣ KIA Stinger\n"
        "5️⃣ Otro / No sé aún"
    ),
    "interes": (
        "Excelente elección 🙌\n\n"
        "¿Cuál es tu presupuesto aproximado?\n\n"
        "1️⃣ Menos de $80 millones\n"
        "2️⃣ Entre $80M y $120M\n"
        "3️⃣ Entre $120M y $180M\n"
        "4️⃣ Más de $180 millones"
    ),
    "presupuesto": (
        "Perfecto 👍\n\n"
        "¿Tienes alguna pregunta adicional o algo específico que quieras saber "
        "sobre el vehículo? (O escribe *no* para continuar)"
    ),
    "done": (
        "✅ ¡Listo, {nombre}!\n\n"
        "Tu información fue enviada a Bryan Losada, quien te contactará muy pronto "
        "para brindarte una atención personalizada. 🚀\n\n"
        "¡Gracias por tu interés en KIA! 🚗💨"
    ),
}

INTEREST_MAP = {
    "1": "KIA Sportage",
    "2": "KIA Picanto",
    "3": "KIA Sonet",
    "4": "KIA Stinger",
    "5": "Otro / No definido",
}

BUDGET_MAP = {
    "1": "Menos de $80M",
    "2": "Entre $80M y $120M",
    "3": "Entre $120M y $180M",
    "4": "Más de $180M",
}

async def handle_message(phone: str, text: str):
    text = text.strip()
    session = await get_session(phone)
    step = session.get("step", "start")
    data = session.get("data", {})

    if step == "start":
        await send_text(phone, MESSAGES["start"])
        await save_session(phone, {"step": "nombre", "data": {"phone": phone}})
        return

    if step == "nombre":
        data["nombre"] = text
        data["phone"] = phone  # JID completo guardado
        msg = MESSAGES["nombre"].format(nombre=text)
        await send_text(phone, msg)
        await save_session(phone, {"step": "interes", "data": data})

    elif step == "interes":
        data["interes"] = INTEREST_MAP.get(text, text)
        await send_text(phone, MESSAGES["interes"])
        await save_session(phone, {"step": "presupuesto", "data": data})

    elif step == "presupuesto":
        data["presupuesto"] = BUDGET_MAP.get(text, text)
        await send_text(phone, MESSAGES["presupuesto"])
        await save_session(phone, {"step": "comentario", "data": data})

    elif step == "comentario":
        data["comentario"] = text if text.lower() != "no" else "Sin comentarios"
        await send_lead_to_bryan(BRYAN_NUMBER, data)
        msg = MESSAGES["done"].format(nombre=data.get("nombre", ""))
        await send_text(phone, msg)
        await clear_session(phone)