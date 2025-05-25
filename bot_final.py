
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time

# Вопросы, варианты и баллы
questions = [
    {
        "text": "Как вы себя идентифицируете в гендерном плане?",
        "options": ["Цисгендер", "Трансгендер", "Небинарная персона", "Никак"],
        "scores": [1, 1, 1, 0]
    },
    {
        "text": "Был ли у вас опыт прохождения реабилитации?",
        "options": ["Да", "Нет"],
        "scores": [1, 0]
    },
    {
        "text": "Вас когда-либо отменяли?",
        "options": ["Да", "Нет"],
        "scores": [1, 0]
    },
    {
        "text": "Вы делали публичный каминг-аут?",
        "options": ["Да", "Нет"],
        "scores": [1, 0]
    },
    {
        "text": "Есть ли у вас татуировки или пирсинг?",
        "options": ["И то, и другое", "Только татуировка", "Только пирсинг", "Нет"],
        "scores": [2, 1, 1, 0]
    }
]

# Храним состояния пользователей
user_data = {}

def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user_data[user_id] = {"current_q": 0, "score": 0}
    send_question(update, context)

def send_question(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    q_index = user_data[user_id]["current_q"]

    if q_index < len(questions):
        q = questions[q_index]
        reply_markup = ReplyKeyboardMarkup.from_row(q["options"], one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(q["text"], reply_markup=reply_markup)
    else:
        score = user_data[user_id]["score"]
        if score <= 3:
            result = (
                "```
"
                "SYSTEM RESPONSE:
"
                "Займись, чем-нибудь другим
"
                "а ха ха ха хахаха ахаха хахаха
"
                "```"
            )
            audio_file = "1.mp3"
        else:
            result = (
                "```
"
                "SYSTEM RESPONSE:
"
                "Ты звезда, в отличие от всех
"
                "```"
            )
            audio_file = "2.mp3"

        context.bot.send_message(chat_id=user_id, text="💾 Инициализация нейронных протоколов...")
        time.sleep(1.2)
        context.bot.send_message(chat_id=user_id, text="⚙️ Анализ входных данных...")
        time.sleep(1.2)
        context.bot.send_message(chat_id=user_id, text="🧠 Расчёт итогового профиля...")
        time.sleep(1.2)
        context.bot.send_message(chat_id=user_id, text="💡 Готово!")
        time.sleep(0.8)
        context.bot.send_message(chat_id=user_id, text=result, parse_mode='Markdown')
        try:
            context.bot.send_audio(chat_id=user_id, audio=open(audio_file, 'rb'))
        except Exception as e:
            context.bot.send_message(chat_id=user_id, text="⚠️ Не удалось отправить аудиофайл.")

        user_data.pop(user_id, None)

def handle_response(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id not in user_data:
        update.message.reply_text("Введите /start для начала теста.")
        return

    q_index = user_data[user_id]["current_q"]
    answer = update.message.text
    q = questions[q_index]

    if answer not in q["options"]:
        update.message.reply_text("Пожалуйста, выберите один из предложенных вариантов.")
        return

    selected_index = q["options"].index(answer)
    user_data[user_id]["score"] += q["scores"][selected_index]
    user_data[user_id]["current_q"] += 1
    send_question(update, context)

def main():
    import os
    TOKEN = os.environ.get("TOKEN")  # <-- Render использует переменную окружения

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_response))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
