# bot_module.py
import asyncpg
from telegram import Bot

DB_CONFIG = {
    "database": "sbp",
    "user": "postgres",
    "password": "2418908595",
    "host": "10.8.0.23",
    "port": "54320"
}
class BotNewsletter():
    def __init__(self,BOT_TOKEN):
        self.bot = Bot(token=BOT_TOKEN)



    async def send_to_users(self, usernames: list[str], text: str):
        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as connection:
                for username in usernames:
                    # Для asyncpg используется $1 вместо ? для параметров
                    user_id = await connection.fetchval(
                        "SELECT user_id FROM tg_acc WHERE username = $1", 
                        username
                    )
                    if user_id:
                        try:
                            await self.bot.send_message(chat_id=user_id, text=text)
                            print(f"Отправлено: {username} ({user_id})")
                        except Exception as e:
                            print(f"Ошибка для {username}: {e}")
