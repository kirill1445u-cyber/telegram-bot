
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Добавь BOT_TOKEN в переменные окружения")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 Статус", callback_data="status"),
        InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
    )
    bot.send_message(
        message.chat.id,
        "🤖 Бот запущен!\n\nВыбери действие в меню:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "status":
        text = "✅ Бот работает."
    elif call.data == "help":
        text = "Используй /start, чтобы открыть меню."
    else:
        text = "Неизвестная команда."

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(message, "Нажми /start, чтобы открыть меню.")

print("Бот запущен")
bot.infinity_polling(skip_pending=True)
