# telegram
Telegram Bot for Weather, Reminders, and Email
This is a simple Telegram bot that offers functionalities like fetching weather information, setting reminders, and sending emails. The bot is built using Python, the python-telegram-bot library, and integrates with the OpenWeather API for weather data.

Features
Weather Information: The bot can provide weather updates for a specified city.

Command: /vreme [city_name]
Set Reminder: You can set a reminder with a specific message to be sent after a specified number of minutes.

Command: /reminder [minutes] [message]
Send Email: The bot can send emails from a Gmail account to a specified recipient.

Command: /email [recipient] [subject] [message]
Help: The bot provides a help message outlining available commands.

Command: /start
Requirements
Python 3.7 or higher
Required Python libraries:
requests
smtplib
python-telegram-bot
asyncio
email.mime.text
You can install these dependencies using pip:

pip install requests python-telegram-bot

Setup
1. Obtain API Keys:
Telegram Bot Token: Create a bot on Telegram via BotFather and get your bot's token.
Weather API Key: Sign up on OpenWeatherMap to get your API key.
2. Configure the Bot:
Update the following variables in the script:

TOKEN = 'your-telegram-bot-token'  # Telegram Bot API token
bot_username = '@YourBotUsername'  # Telegram bot username
WEATHER_API_KEY = 'your-weather-api-key'  # OpenWeatherMap API key
SENDER_EMAIL = 'your-email@gmail.com'  # Your email address (Gmail recommended)
SENDER_PASSWORD = 'your-email-password'  # Your email password (use app-specific password if needed)
DEFAULT_RECIPIENT = 'recipient@example.com'  # Default email recipient
3. Running the Bot:
Once you've configured the bot, run the Python script:

python bot_script.py
The bot will start and run in polling mode, awaiting user input.

4. Commands Overview
/start: Shows a help message with a list of available commands.
/vreme [city_name]: Fetches and displays the current weather of the specified city.
/reminder [minutes] [message]: Sets a reminder to notify the user after the specified number of minutes.
/email [recipient] [subject] [message]: Sends an email with the specified subject and message to the recipient.
License
This bot is open-source and free to use. However, make sure to protect your sensitive credentials such as API keys and email passwords before using it in production.
