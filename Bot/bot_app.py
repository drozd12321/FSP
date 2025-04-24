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
    """Класс для рассылки сообщений пользователям Telegram через бота.
    
    Использует базу данных PostgreSQL для получения user_id по username
    и Telegram Bot API для отправки сообщений.
    
    Attributes:
        bot (Bot): Экземпляр телеграм-бота для отправки сообщений.
    """
    def __init__(self,BOT_TOKEN):
        """Инициализирует экземпляр бота для рассылки.
        
        Args:
            BOT_TOKEN (str): Токен Telegram бота, полученный от @BotFather.
        """
        self.bot = Bot(token=BOT_TOKEN)



    async def send_to_users(self, usernames: list[str], text: str):
        """Отправляет текстовое сообщение списку пользователей Telegram.
        
        Для каждого username из списка находит соответствующий user_id в базе данных,
        затем отправляет сообщение через Telegram Bot API.
        
        Args:
            usernames (list[str]): Список username пользователей (без @).
            text (str): Текст сообщения для рассылки.
            
        Note:
            Логирует результат отправки или ошибки в stdout.
            Требует наличия таблицы tg_acc с колонками user_id и username в БД.
        """
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
