from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Состояния диалога
MENU, GET_INFO = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога с текстовым меню"""
    menu_text = (
        "Выбери программу (отправь цифру):\n"
        "1. Искусственный интеллект\n"
        "2. AI-продукты\n"
        "3. Сравнить программы"
    )
    await update.message.reply_text(menu_text)
    return MENU

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора программы по цифре"""
    choice = update.message.text
    
    if choice == "1":
        program = "Искусственный интеллект"
    elif choice == "2":
        program = "AI-продукты"
    elif choice == "3":
        await update.message.reply_text(
            "Сравнение программ:\n\n"
            "1. Искусственный интеллект - для разработчиков алгоритмов\n"
            "2. AI-продукты - для менеджеров продуктов\n\n"
            "Для выбора программы нажми /start"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, выбери цифру от 1 до 3")
        return MENU
    
    context.user_data['program'] = program
    await update.message.reply_text(
        f"Выбрано: {program}\n\n"
        "Теперь расскажи о своем опыте:\n"
        "- Образование\n"
        "- Навыки\n"
        "- Интересы"
    )
    return GET_INFO

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получение информации о пользователе"""
    experience = update.message.text
    program = context.user_data['program']
    
    if "интеллект" in program:
        response = (
            "Рекомендации по ИИ:\n"
            "1. Машинное обучение\n"
            "2. Нейросети\n"
            "3. Обработка данных"
        )
    else:
        response = (
            "Рекомендации по продуктам:\n"
            "1. Управление продуктами\n"
            "2. Маркетинг\n"
            "3. Бизнес-аналитика"
        )
    
    await update.message.reply_text(
        f"Спасибо! Вот рекомендации:\n\n{response}\n\n"
        "Для нового выбора нажми /start"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    await update.message.reply_text(
        "Диалог завершен. Нажми /start для начала.",
    )
    return ConversationHandler.END

def main():
    """Запуск бота"""
    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            GET_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    app.add_handler(conv_handler)
    print("Бот запущен! Используй /start в Telegram")
    app.run_polling()

if __name__ == '__main__':
    main()