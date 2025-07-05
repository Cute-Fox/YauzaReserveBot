from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service
from bot.async_app import schedule


def register(bot: TeleBot, sessionmaker: async_sessionmaker) -> None:
    @bot.message_handler(commands=["my_id"])
    def handle_setadmin(message: types.Message):
        async def _reply_id():
            async with sessionmaker() as session:
                bot.reply_to(message, f"Ваш ID: {message.from_user.id}\nИспользуйте его для изменения статуса.")

        schedule(_reply_id())