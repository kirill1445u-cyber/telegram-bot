
import os
import logging
from datetime import datetime, timezone

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

COUNTRIES = {
    "ru": "🇷🇺 Россия",
    "in": "🇮🇳 Индия",
    "bd": "🇧🇩 Бангладеш",
    "us": "🇺🇸 США",
    "jp": "🇯🇵 Япония",
}

stats = {"starts": 0, "checks": 0}


def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔎 Найти номер", callback_data="countries"),
            InlineKeyboardButton("📊 Статус", callback_data="status"),
        ],
        [
            InlineKeyboardButton("📈 Статистика", callback_data="stats"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help"),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats["starts"] += 1
    await update.message.reply_text(
        "🤖 БОТ АВТОРЕГИСТРАЦИИ\n\n"
        "Выбери действие в меню.\n\n"
        "🔎 Выбор страны\n"
        "📊 Статус бота\n"
        "📈 Статистика",
        reply_markup=main_menu(),
    )


async def show_countries(query):
    keyboard = [
        [InlineKeyboardButton(
            name, callback_data=f"country:{code}"
        )]
        for code, name in COUNTRIES.items()
    ]
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад", callback_data="home")
    ])
    await query.edit_message_text(
        "🌍 Выбери страну:\n\n"
        "Для поиска реальных номеров потребуется API поставщика.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.edit_message_text(
            "🤖 Главное меню",
            reply_markup=main_menu(),
        )

    elif data == "countries":
        await show_countries(query)

    elif data.startswith("country:"):
        code = data.split(":", 1)[1]
        name = COUNTRIES.get(code)
        if not name:
            await query.edit_message_text("Неизвестная страна.")
            return

        stats["checks"] += 1
        await query.edit_message_text(
            f"{name}\n\n"
            "⚠️ Реальный поиск пока не подключён.\n"
            "Добавь API поставщика номеров, чтобы получать "
            "актуальную доступность и заказы.\n\n"
            "Бот не будет показывать выдуманные номера или коды.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "⬅️ К странам", callback_data="countries"
                ),
                InlineKeyboardButton(
                    "🏠 Меню", callback_data="home"
                ),
            ]]),
        )

    elif data == "status":
        await query.edit_message_text(
            "✅ Бот отвечает.\n"
            f"🕒 Время сервера: "
            f"{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}\n"
            "🔌 Поиск номеров: API не подключён.",
            reply_markup=main_menu(),
        )

    elif data == "stats":
        await query.edit_message_text(
            "📊 СТАТИСТИКА\n\n"
            f"▶️ Запусков команды /start: {stats['starts']}\n"
            f"🔎 Запросов стран: {stats['checks']}\n"
            "📡 API номеров: не подключён",
            reply_markup=main_menu(),
        )

    elif data == "help":
        await query.edit_message_text(
            "ℹ️ ПОМОЩЬ\n\n"
            "/start — открыть меню\n"
            "/help — помощь\n\n"
            "Выбери страну в меню. Для реального поиска "
            "нужен API поставщика. Коды следует получать "
            "только для регистраций, которые ты сам инициировал.",
            reply_markup=main_menu(),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Нажми /start, чтобы открыть меню."
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "Не задан BOT_TOKEN в переменных окружения Bothost"
        )

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))
    log.info("Bot starting")
    app.run_polling()


if __name__ == "__main__":
    main()
