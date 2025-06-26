from telebot import TeleBot
from bot.config import get_settings

settings = get_settings()
bot = TeleBot(settings.bot_token, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Бот запущен и работает 🐾")


def run():
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    run()
