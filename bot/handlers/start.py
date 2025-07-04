from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service
from bot.async_app import schedule
from bot.utils.keyboards import main_menu

def register(bot: TeleBot, sessionmaker: async_sessionmaker) -> None:
    @bot.message_handler(commands=["start"])
    def handle_start(message: types.Message):
        tg_id = message.from_user.id

        async def _reply():
            async with sessionmaker() as session:
                user = await user_service.get_user(session, tg_id)
                if user:
                    bot.send_message(message.chat.id, f"С возвращением, {user.name}!\nВыберите действие из меню.", reply_markup=main_menu())
                else:
                    msg = bot.send_message(message.chat.id, "Привет! Как мне к вам обращаться?")
                    bot.register_next_step_handler(msg, save_name)

        schedule(_reply())  

    def save_name(message: types.Message):
        tg_id = message.from_user.id
        name = message.text.strip()

        if not name.isalpha() or len(name) < 2:
            nxt = bot.send_message(message.chat.id, "Пожалуйста, введите корректное имя.")
            bot.register_next_step_handler(nxt, save_name)
            return

        async def _save():
            async with sessionmaker() as session:
                await user_service.save_user(session, tg_id, name)
        schedule(_save())
        bot.send_message(message.chat.id, f"Приятно познакомиться, {name}!\nТеперь ты можешь выбрать действие из меню.", reply_markup=main_menu())
