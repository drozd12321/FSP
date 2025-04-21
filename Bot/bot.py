import asyncio
import asyncpg
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Параметры подключения к PostgreSQL
DB_CONFIG = {
    "database": "sbp",
    "user": "postgres",
    "password": "2418908595",
    "host": "10.8.0.23",
    "port": "54320"
}

# Инициализация базы данных
async def init_db():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tg_acc (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE,
                user_id BIGINT
            )
        """)
    finally:
        await conn.close()

# Сохраняем нового пользователя
async def save_user(username: str, user_id: int):
    if not username:
        return  # игнорируем без username
    
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        await conn.execute("""
            INSERT INTO tg_acc (username, user_id) 
            VALUES ($1, $2)
            ON CONFLICT (username) DO NOTHING
        """, username, user_id)
    finally:
        await conn.close()

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await save_user(user.username, user.id)
    print(f"Новый пользователь: {user.username} — {user.id}")
    await update.message.reply_text("Привет! Ты подписался на рассылку от ФСП.\nДля просмотра соревнований, в которых ты учавствуешь используй /send")

# Обработчик /send
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_user.id
    sender_username = update.effective_user.username  # может быть None, если username не установлен
    conn = await asyncpg.connect(**DB_CONFIG)
    competitions = False
    try:
        user_id = await conn.fetchval(
            "SELECT user_id FROM tg_acc WHERE username = $1", 
            sender_username
        )
        if user_id and competitions:
            try:
                await context.bot.send_message(chat_id=user_id, text="Привет! Ты учавствуешь в соревнованиях ...")
                print(f"Отправлено: {sender_username} ({user_id})")
            except Exception as e:
                print(f"Ошибка для {sender_username}: {e}")
        else:
            await context.bot.send_message(chat_id=user_id, text="Привет! Ты пока нигде не учавствуешь")
    finally:
        await conn.close()


# Основная функция
async def main():
    await init_db()
    app = Application.builder().token("7396130456:AAG8C8b5R1A_eKGgsbOmjXQ93039wKbSbkQ").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", broadcast))
    await app.run_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())