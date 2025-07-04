from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service, manager_chat_service
from bot.async_app import schedule


def register(bot: TeleBot, sm: async_sessionmaker):
    @bot.message_handler(commands=["addchat"])
    def add_manager_chat(message: types.Message):
        if message.chat.type == "private":
            return bot.reply_to(message, "Эту команду нужно вызвать *в самом групповом чате*.")

        async def _add():
            async with sm() as s:
                me = await user_service.get_user(s, message.from_user.id)
                if not (me and me.is_admin):
                    return bot.reply_to(message, "Только админ может добавлять чаты.")

                await manager_chat_service.add_chat(s, message.chat.id, message.chat.title)
                bot.reply_to(message, "Чат зарегистрирован ✅")

        schedule(_add())

    @bot.message_handler(commands=["delchat"])
    def remove_manager_chat(message: types.Message):
        if message.chat.type == "private":
            return bot.reply_to(message, "Эту команду нужно вызвать *в самом групповом чате*.")

        async def _remove():
            async with sm() as s:
                me = await user_service.get_user(s, message.from_user.id)
                if not (me and me.is_admin):
                    return bot.reply_to(message, "Только админ может удалять чаты.")

                await manager_chat_service.remove_chat(s, message.chat.id)
                bot.reply_to(message, "Чат удалён ✅")

        schedule(_remove())
