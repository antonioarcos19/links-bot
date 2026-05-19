import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8262475296:AAFgC213ydlPrlxYKA8yTRTVlHtzK7NFyYI"
CANAL_ID = -1003834984155
GRUPO_ID = -1003918749962

logging.basicConfig(level=logging.INFO)

async def verificar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    user_id = message.from_user.id

    # Verificar si es miembro del canal
    try:
        member = await context.bot.get_chat_member(CANAL_ID, user_id)
        es_miembro = member.status in ["member", "administrator", "creator"]
    except:
        es_miembro = False

    # Si no es miembro, borrar mensaje y avisar
    if not es_miembro:
        await message.delete()
        await context.bot.send_message(
            chat_id=GRUPO_ID,
            text=(
                f"⚠️ {message.from_user.first_name}, para enviar enlaces aquí "
                f"primero debes unirte a nuestro canal:\n\n"
                f"👉 https://t.me/titesbets"
            )
        )
        return

    # Si es miembro pero no es un enlace, borrar el mensaje
    if not message.text or ("http://" not in message.text and "https://" not in message.text):
        await message.delete()
        await context.bot.send_message(
            chat_id=GRUPO_ID,
            text=f"❌ {message.from_user.first_name}, solo se permiten enlaces en este grupo."
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, verificar_mensaje))
app.run_polling()
