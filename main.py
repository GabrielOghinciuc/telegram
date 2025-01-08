import requests
import smtplib
import asyncio
from email.mime.text import MIMEText
from telegram import Update
from telegram.ext import MessageHandler,  Application, CommandHandler, ContextTypes
from telegram.ext.filters import TEXT, COMMAND
import logging

# Token și username bot
TOKEN = '7241278780:AAGFQCYc_Um6tDtDYQHe99LfxAjZuatauOw'
bot_username = '@DorelSmartBot'

# API pentru vreme
WEATHER_API_KEY = ''
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Detalii pentru trimiterea unui email
SENDER_EMAIL = ""  
SENDER_PASSWORD = ''
DEFAULT_RECIPIENT = "idkmlbb2004@gmail.com"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Imi pare rau, dar nu înțeleg comanda sau textul scris. Încearcă /start pentru ajutor!"
        )

async def handle_unexpected_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Nu pot intelege comanda ta. Incearca una dintre comenzile disponibile, cum ar fi /vreme sau /email."
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        f"Salut! Sunt {bot_username}! \nCum te pot ajuta?\n\n"
        "Lista comenzilor disponibile:\n"
        "/vreme [oraș] - Afișează vremea pentru un oraș.\n"
        "/reminder [minute] [mesaj] - Setează un reminder pentru un anumit timp.\n"
        "/email [destinatar] [subiect] [mesaj] - Trimite un email.(Subiectul sa fie doar de un cuvant!!!)\n"
    )
    await update.message.reply_text(help_text)

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = ' '.join(context.args).strip()
    if not city:
        await update.message.reply_text("Te rog să specifici un oraș! Folosește comanda astfel: /vreme [oraș].")
        return
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
        )
        data = response.json()
        if response.status_code == 200 and 'main' in data:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            await update.message.reply_text(f"Temperatura în {city} este {temp}°C. {description.capitalize()}.")
        else:
            error_message = data.get("message", "Eroare necunoscută")
            await update.message.reply_text(f"Nu am gasit informatii pentru {city}. Detalii: {error_message}")
    except Exception as e:
        await update.message.reply_text(f"A aparut o eroare la procesarea cererii: {e}")

# Funcție pentru a seta un reminder
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        time = int(context.args[0])
        reminder_message = ' '.join(context.args[1:])
        if time <= 0 or not reminder_message:
            await update.message.reply_text("Te rog să specifici un timp posibil(minute > 0) și un mesaj.")
            return
        await update.message.reply_text(f"Reminderul tau a fost setat pentru {time} minute.")
        await asyncio.sleep(time * 60)
        await update.message.reply_text(f"Reminder: {reminder_message}")
    except (IndexError, ValueError):
        await update.message.reply_text("Foloseste comanda astfel: /reminder [minute] [mesaj]")

# Funcție pentru a trimite un email
async def send_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        recipient = context.args[0] if context.args else DEFAULT_RECIPIENT
        subject = context.args[1] if len(context.args) > 1 else "Subiectul nu a fost specificat"
        message = ' '.join(context.args[2:]) if len(context.args) > 2 else "Mesajul nu a fost specificat"

        # Creăm mesajul email
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient

        # Trimiterea emailului
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        
        await update.message.reply_text(f"Emailul a fost trimis cu succes catre {recipient}.")
    except Exception as e:
        await update.message.reply_text(f"Eroare la trimiterea emailului: {e}")

# Main pentru bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Comenzi pentru bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vreme", get_weather))
    application.add_handler(CommandHandler("reminder", set_reminder))
    application.add_handler(CommandHandler("email", send_email))
    # Handler pentru comenzi necunoscute
    application.add_handler(MessageHandler(COMMAND, unknown_command))
    # Handler pentru mesaje neașteptate
    application.add_handler(MessageHandler(TEXT & ~COMMAND, handle_unexpected_message))

    application.run_polling()

if __name__ == "__main__":
    main()
