import asyncio
from bot_app import BotNewsletter

BOT_TOKEN = "YOU_TOKEN"

async def main(usernames):
    """Асинхронная функция для запуска рассылки сообщений через Telegram бота.
    
    Создает экземпляр BotNewsletter и отправляет заданное сообщение
    списку пользователей.
    
    Args:
        usernames (list): Список username пользователей Telegram (без @) для рассылки.
        
    Example:
        Рассылка сообщения двум пользователям:
        >>> asyncio.run(main(['flymalysh', 'Ainsfari']))
    """
    newsletter = BotNewsletter(BOT_TOKEN)
    message = "Привет, это сообщение отправлено вне Telegram."

    await newsletter.send_to_users(usernames, message)

if __name__ == "__main__":
    asyncio.run(main(['flymalysh', 'Ainsfari']))
