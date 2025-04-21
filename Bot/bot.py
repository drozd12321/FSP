import asyncio
import asyncpg
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await save_user(user.username, user.id)
    print(f"Новый пользователь: {user.username} — {user.id}")

    keyboard = [
        ["📅 Мои соревнования", "ℹ️ Помощь"],
        ["⚙️ Настройки", "📌 О боте"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        "Ты успешно подписался на рассылку от ФСП."
        "Этот бот помогает отслеживать соревнования ФСП, а таже искать команды под свой скилл.\n\n"
        "Выбери нужное действие:",
        reply_markup=reply_markup,
    )

async def get_user_competitions(user_id: int):
    """Функция для получения соревнований пользователя из БД"""
    print('подкл')
    conn = await asyncpg.connect(**DB_CONFIG)
    print('ищу')
    try:
        # Здесь ваша логика запроса к базе данных
        competitions = await conn.fetch(
            "SELECT * FROM win_competition WHERE id = $1", 
            user_id
        )
        return competitions if competitions else None
    finally:
        await conn.close()

async def handle_competitions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки 'Мои соревнования'"""
    user = update.effective_user
    loading_msg = await update.message.reply_text("⏳ Загружаю список соревнований...")
    
    try:
        # Получаем user_id из вашей основной таблицы пользователей
        conn = await asyncpg.connect(**DB_CONFIG)
        user_id = await conn.fetchval(
            "SELECT user_id FROM tg_acc WHERE user_id = $1", 
            user.id
        )
        
        if user_id:
            competitions = await get_user_competitions(user_id)
            
            if competitions:
                response = "🏆 Твои соревнования:\n\n" + "\n".join(
                    f"• {comp['name']} ({comp['date']})" 
                    for comp in competitions
                )
            else:
                response = "🤷 Ты пока не участвуешь ни в каких соревнованиях"
        else:
            response = "🔍 Не удалось найти твой аккаунт в системе"
        
        await loading_msg.edit_text(response)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        await loading_msg.edit_text("😞 Произошла ошибка при загрузке данных")
    finally:
        await conn.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📅 Мои соревнования":
        await handle_competitions(update, context)
    elif text == "ℹ️ Помощь":
        await update.message.reply_text('''
Вот список доступных команд:
''')
    elif text == "⚙️ Настройки":
        await update.message.reply_text("Здесь будут настройки...")
    elif text == "📌 О боте":
        await update.message.reply_text("Бот от команды Аналитик!\nЭтот бот помогает отслеживать соревнования ФСП, а таже искать команды под свой скилл.")

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
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