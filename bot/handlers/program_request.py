from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from datetime import datetime

from bot.services import user_service
from bot.utils.notifier import notify_managers
from bot.utils.keyboards import main_menu
from bot.async_app import schedule


def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    @bot.message_handler(func=lambda m: m.text == "📅 Программа недели")
    @bot.message_handler(commands=["program"])
    def handle_program_request(message: types.Message):
        tg_id = message.from_user.id

        async def _process():
            async with sm() as session:
                user = await user_service.get_user(session, tg_id)

            text = (
                "🆕 Заявка на программу мероприятий!\n\n"
                f"Дата запроса: {datetime.utcnow():%d.%m.%Y %H:%M UTC}\n\n"
                f"Клиент: {user.name}\n"
                f"TG-ID: {tg_id}\n"
                f"Username: @{message.from_user.username or '—'}\n\n"
                "⏳ Пожалуйста, уточните детали и вышлите расписание."
            )
            notify_managers(bot, sm, text)

            bot.send_message(
                message.chat.id,
                "Ваша заявка на получение программы недели передана менеджеру.\n"
                "Мы уточним пару моментов и свяжемся с вами!",
                reply_markup=main_menu()
            )

        schedule(_process())
