# external_sender.py

import asyncio

from bot_app import BotNewsletter

# Токен от BotFather
BOT_TOKEN = "7396130456:AAG8C8b5R1A_eKGgsbOmjXQ93039wKbSbkQ"

async def main(usernames):
    
    newsletter = BotNewsletter(BOT_TOKEN)
    message = "Привет, это сообщение отправлено вне Telegram чата."

    await newsletter.send_to_users(usernames, message)

if __name__ == "__main__":
    asyncio.run(main(['flymalysh', 'Ainsfari']))
