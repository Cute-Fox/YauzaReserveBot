from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.services import user_service
from bot.async_app import schedule

def register(bot: TeleBot, sessionmaker: async_sessionmaker) -> None:
    @bot.message_handler(func=lambda m: True, pass_bot_commands=True)
    def middleware(message: types.Message) -> None:
        tg_id = message.from_user.id

        async def _check() -> None:
            async with sessionmaker() as session:
                user = await user_service.get_user(session, tg_id)
                if user:
                    return

                ask = bot.send_message(
                    message.chat.id,
                    "Как мне к вам обращаться?"
                )
                bot.register_next_step_handler(ask, save_name)

        schedule(_check())                 
    
    def save_name(message: types.Message) -> None:
        tg_id = message.from_user.id
        name = message.text.strip()

        if not name.isalpha() or len(name) < 2 or len(name) > 100:
            retry = bot.send_message(
                message.chat.id,
                "Пожалуйста, введите имя буквами (минимум 2, максимум 100)."
            )
            bot.register_next_step_handler(retry, save_name)
            return

        async def _save() -> None:
            async with sessionmaker() as session:
                await user_service.save_user(session, tg_id, name)

        schedule(_save())
        bot.send_message(message.chat.id, f"Приятно познакомиться, {name}!")
