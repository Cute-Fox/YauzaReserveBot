from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service, setting_service
from bot.async_app import schedule


def register(bot: TeleBot, sm: async_sessionmaker) -> None:
    @bot.message_handler(commands=["setcontact"])
    def handle_setcontact(message: types.Message):
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "Используйте: /setcontact (телефон) (имя)")
            return

        phone, name = parts[1], parts[2]
        admin_id     = message.from_user.id

        async def _save():
            async with sm() as s:
                me = await user_service.get_user(s, admin_id)
                if not (me and me.is_admin):
                    bot.reply_to(message, "Только админ может менять контакты!")
                    return
                await setting_service.set_(s, "admin_phone", phone)
                await setting_service.set_(s, "admin_name", name)
                bot.reply_to(message, "Контакт админа обновлён ✅")

        schedule(_save())
