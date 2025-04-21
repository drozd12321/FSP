# external_sender.py

import asyncio
from telegram import Bot
from bot_app import send_to_users  # Импортируй оттуда, где у тебя функция

# Токен от BotFather
BOT_TOKEN = "7396130456:AAG8C8b5R1A_eKGgsbOmjXQ93039wKbSbkQ"

async def main():
    bot = Bot(token=BOT_TOKEN)
    
    usernames = ['flymalysh', 'Ainsfari']  # Замени на актуальные логины
    message = "Привет, это сообщение отправлено вне Telegram чата."

    await send_to_users(bot, usernames, message)

if __name__ == "__main__":
    asyncio.run(main())
