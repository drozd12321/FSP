import asyncio
import asyncpg
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

# Параметры подключения к PostgreSQL
DB_CONFIG = {
    "database": "sbp",
    "user": "postgres",
    "password": "2418908595",
    "host": "10.8.0.23",
    "port": "54320"
}


# Определяем состояния для FSM
QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4, QUESTION_5, QUESTION_6 = range(6)

async def find_competitions_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало опроса - первый вопрос"""
    context.user_data['answers'] = {}
    
    keyboard = [
        ["🧑‍💻 Продуктовое программирование", "🛡️ Программирование систем ИБ"],
        ["🤖 Программирование робототехники", "🧠 Алгоритмическое программирование"],
        ["✈️ Программирование беспилотных авиационных систем"]
    ]
    await update.message.reply_text(
        "🏆 Давай найдем подходящие соревнования!\n"
        "Какая дисциплина тебя интересует?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return QUESTION_1

async def handle_question_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка первого вопроса"""
    context.user_data['answers']['discipline'] = update.message.text
    
    keyboard = [["Онлайн", "Офлайн", "Все"]]
    await update.message.reply_text(
        "Вас интересуют онлайн или офлайн участие?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return QUESTION_2

async def handle_question_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка второго вопроса"""
    context.user_data['answers']['format'] = update.message.text
    
    keyboard = [["Региональные", "Всероссийские"]]
    await update.message.reply_text(
        "Выберите масштаб соревнований:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return QUESTION_3

async def handle_question_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка третьего вопроса"""
    context.user_data['answers']['scale'] = update.message.text
    
    # Всегда переходим к вопросу о возрасте, независимо от выбора
    await update.message.reply_text(
        "Укажи свой возраст:",
        reply_markup=ReplyKeyboardRemove()
    )
    return QUESTION_4

async def handle_question_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка вопроса о возрасте"""
    try:
        age = int(update.message.text)
        if age < 10 or age > 100:
            await update.message.reply_text("Пожалуйста, укажи реальный возраст (от 10 до 100 лет):")
            return QUESTION_4
        context.user_data['answers']['age'] = age
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число (твой возраст):")
        return QUESTION_4
    
    # Добавляем новый вопрос об уровне подготовки
    keyboard = [["Индивидуальные", "Командные"]]
    await update.message.reply_text(
        "Выбери тип соревнований",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return QUESTION_5  # Переходим к новому вопросу

async def handle_question_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка вопроса об уровне подготовки"""
    context.user_data['answers']['type'] = update.message.text
    
    # Если выбраны региональные, спрашиваем регион
    if context.user_data['answers'].get('scale') == "Региональные":
        await update.message.reply_text("Укажи, из какого ты региона:")
        return QUESTION_6
    
    # Иначе завершаем опрос
    return await finish_questionnaire(update, context)

async def handle_question_6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка вопроса о регионе (только для региональных)"""
    region = update.message.text
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        # Здесь ваша логика запроса к базе данных
        competitions = await conn.fetch(
            "SELECT * FROM win_region WHERE name = $1", 
            region
        )
        print(competitions)
        if competitions:
            context.user_data['answers']['region'] = update.message.text
            return await finish_questionnaire(update, context)
        else:
            await update.message.reply_text("Вы ввели неверное название региона.\nВведите заново (например: Республика Татарстан):")
            return await QUESTION_6
    finally:
        await conn.close()
    # context.user_data['answers']['region'] = update.message.text
    

async def finish_questionnaire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение опроса и вывод результатов"""
    answers = context.user_data['answers']
    
    report = (
        "📋\n"
        f"• Дисциплина: {answers.get('discipline', 'Не указано')}\n"
        f"• Формат: {answers.get('format', 'Не указано')}\n"
        f"• Масштаб: {answers.get('scale', 'Не указано')}\n"
        f"• Возраст: {answers.get('age', 'Не указано')}\n"
        f"• Тип соревнований: {answers.get('type', 'Не указано')}\n"
    )
    
    if 'region' in answers:
        report += f"• Регион: {answers['region']}\n"
    
    keyboard = [
        ["📅 Мои соревнования", "🏆 Найти соревнования"],
        ["ℹ️ Помощь", "📌 О боте"],
    ]
    await update.message.reply_text(
        f"{report}\n\nИщем подходящие варианты...",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена опроса"""
    keyboard = [
        ["📅 Мои соревнования", "🏆 Найти соревнования"],
        ["ℹ️ Помощь", "📌 О боте"],
    ]
    await update.message.reply_text(
        "Опрос отменен",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

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
        ["📅 Мои соревнования", "🏆 Найти соревнования"],
        ["ℹ️ Помощь", "📌 О боте"],
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
    conn = await asyncpg.connect(**DB_CONFIG)
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
                response = "🤷 Ты пока не участвуешь ни в каких соревнованиях.\nСкорее заходи на сайт и учавствуй!\nhttp://10.8.0.6:5173/"
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
    elif text == "🏆 Найти соревнования":
        # Запускаем опрос
        return await find_competitions_start(update, context)
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
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("🏆 Найти соревнования"), find_competitions_start)],
        states={
            QUESTION_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_1)],
            QUESTION_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_2)],
            QUESTION_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_3)],
            QUESTION_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_4)],
            QUESTION_5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_5)],
            QUESTION_6: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question_6)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.Text(["Отмена", "Вернуться"]), cancel)
        ],
    )
    app.add_handler(conv_handler)
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