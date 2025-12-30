import requests
import smtplib
import asyncio
from email.mime.text import MIMEText
from telegram import Update
from telegram.ext import MessageHandler,  Application, CommandHandler, ContextTypes
from telegram.ext.filters import TEXT, COMMAND
import logging

TOKEN = '7241278780:AAGFQCYc_Um6tDtDYQHe99LfxAjZuatauOw'
bot_username = '@DorelSmartBot'

# API pentru vreme
WEATHER_API_KEY = '0778fa7de75c6e39732bb45faf7e7e72'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Detalii pentru trimiterea unui email
SENDER_EMAIL = "idkmlbb2004@gmail.com"  
SENDER_PASSWORD = 'xjxi gcru fcls ajpn'
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
        "/catfact - Obține un fapt amuzant despre pisici.\n"
        "/dog - Primește o imagine random cu un câine.\n"
        "/chuck - Primește o glumă cu Chuck Norris.\n"
        "/ipinfo [adresa IP] - Informații despre o adresă IP.\n"
        "/quote - Primește un citat motivațional.\n"
        "/exchange [suma] [din] [in] - Convertor valutar (ex: /exchange 100 USD EUR).\n"
        "/dadjoke - Primește o glumă de tată.\n"
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

async def send_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        recipient = context.args[0] if context.args else DEFAULT_RECIPIENT
        subject = context.args[1] if len(context.args) > 1 else "Subiectul nu a fost specificat"
        message = ' '.join(context.args[2:]) if len(context.args) > 2 else "Mesajul nu a fost specificat"

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

async def cat_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get('https://catfact.ninja/fact')
        data = response.json()
        if response.status_code == 200 and 'fact' in data:
            await update.message.reply_text(f"🐱 Fapt despre pisici:\n{data['fact']}")
        else:
            await update.message.reply_text("Nu am putut obține un fapt despre pisici.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def dog_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        if response.status_code == 200 and data.get('status') == 'success':
            await update.message.reply_photo(photo=data['message'])
        else:
            await update.message.reply_text("Nu am putut obține o imagine cu câini.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def chuck_norris_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get('https://api.chucknorris.io/jokes/random')
        data = response.json()
        if response.status_code == 200 and 'value' in data:
            await update.message.reply_text(f"😎 Chuck Norris:\n{data['value']}")
        else:
            await update.message.reply_text("Nu am putut obține o glumă cu Chuck Norris.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ip = ' '.join(context.args).strip() if context.args else ''
        if not ip:
            # Dacă nu se specifică IP, obține IP-ul utilizatorului
            response = requests.get('https://api.ipify.org?format=json')
            ip = response.json()['ip']
        
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        
        if response.status_code == 200 and 'city' in data:
            info = (
                f"🌍 Informații despre IP: {ip}\n"
                f"Țară: {data.get('country_name', 'N/A')} ({data.get('country', 'N/A')})\n"
                f"Oraș: {data.get('city', 'N/A')}\n"
                f"Regiune: {data.get('region', 'N/A')}\n"
                f"Coordonate: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n"
                f"Provider: {data.get('org', 'N/A')}"
            )
            await update.message.reply_text(info)
        else:
            await update.message.reply_text(f"Nu am putut obține informații despre IP-ul {ip}.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get('https://api.quotable.io/random')
        data = response.json()
        if response.status_code == 200 and 'content' in data:
            quote = f"💭 \"{data['content']}\"\n\n- {data['author']}"
            await update.message.reply_text(quote)
        else:
            await update.message.reply_text("Nu am putut obține un citat.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def currency_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3:
            await update.message.reply_text(
                "Folosește comanda astfel: /exchange [suma] [din] [in]\n"
                "Exemplu: /exchange 100 USD EUR"
            )
            return
        
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()
        
        response = requests.get(
            f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
        )
        data = response.json()
        
        if response.status_code == 200 and 'rates' in data:
            if to_currency in data['rates']:
                rate = data['rates'][to_currency]
                result = amount * rate
                await update.message.reply_text(
                    f"💱 {amount} {from_currency} = {result:.2f} {to_currency}\n"
                    f"Rata de schimb: 1 {from_currency} = {rate:.4f} {to_currency}"
                )
            else:
                await update.message.reply_text(f"Moneda {to_currency} nu este validă.")
        else:
            await update.message.reply_text(f"Nu am putut obține rata de schimb pentru {from_currency}.")
    except ValueError:
        await update.message.reply_text("Suma trebuie să fie un număr valid.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

async def dad_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
        data = response.json()
        if response.status_code == 200 and 'joke' in data:
            await update.message.reply_text(f"😄 {data['joke']}")
        else:
            await update.message.reply_text("Nu am putut obține o glumă.")
    except Exception as e:
        await update.message.reply_text(f"Eroare: {e}")

# Main pentru bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Comenzi pentru bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vreme", get_weather))
    application.add_handler(CommandHandler("reminder", set_reminder))
    application.add_handler(CommandHandler("email", send_email))
    application.add_handler(CommandHandler("catfact", cat_fact))
    application.add_handler(CommandHandler("dog", dog_image))
    application.add_handler(CommandHandler("chuck", chuck_norris_joke))
    application.add_handler(CommandHandler("ipinfo", ip_info))
    application.add_handler(CommandHandler("quote", random_quote))
    application.add_handler(CommandHandler("exchange", currency_exchange))
    application.add_handler(CommandHandler("dadjoke", dad_joke))
    # Handler pentru comenzi necunoscute
    application.add_handler(MessageHandler(COMMAND, unknown_command))
    # Handler pentru mesaje neașteptate
    application.add_handler(MessageHandler(TEXT & ~COMMAND, handle_unexpected_message))

    application.run_polling()

if __name__ == "__main__":
    main()
