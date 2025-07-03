from telebot import TeleBot, types
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service
from bot.async_app import schedule


def register(bot: TeleBot, sessionmaker: async_sessionmaker) -> None:
    @bot.message_handler(commands=["setadmin"])
    def handle_setadmin(message: types.Message):
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            bot.reply_to(message, "Использование: /setadmin (telegram_id)")
            return

        requester_id = message.from_user.id
        target_id    = int(args[1])

        async def _set():
            async with sessionmaker() as session:
                me = await user_service.get_user(session, requester_id)
                if not (me and me.is_admin):
                    bot.reply_to(message, "Только администратор может назначать админов.")
                    return

                target = await user_service.get_user(session, target_id)
                if not target:
                    bot.reply_to(message, "Пользователь ещё не регистрировался.")
                    return

                await user_service.set_admin(session, target_id, True)
                bot.reply_to(message, f"Пользователь {target.name} назначен админом ✅")

        schedule(_set())
