from telebot import TeleBot
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service, manager_chat_service
from bot.async_app import schedule


def notify_managers(bot: TeleBot,
                    sm: async_sessionmaker,
                    text: str) -> None:

    async def _send():
        async with sm() as s:
            # лички
            admin_ids = await user_service.get_admin_ids(s)
            # групповые чаты
            chat_ids  = await manager_chat_service.all_chat_ids(s) 
        targets = set(admin_ids + chat_ids)

        for cid in targets:
            try:
                bot.send_message(cid, text)
            except Exception:
                pass

    schedule(_send())