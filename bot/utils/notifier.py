import asyncio
from telebot import TeleBot
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.services import user_service, manager_chat_service

def notify_managers(bot: TeleBot, sm: async_sessionmaker, text: str) -> None:
    async def get_all_ids():
        async with sm() as s:
            admin_ids = await user_service.get_admin_ids(s)
            chat_ids = await manager_chat_service.all_chat_ids(s)
        return list(set(admin_ids + chat_ids))

    try:
        loop = asyncio.get_running_loop()
        async def async_notify():
            chat_ids = await get_all_ids()
            for cid in chat_ids:
                try:
                    bot.send_message(cid, text)
                except Exception:
                    pass
        asyncio.create_task(async_notify())
    except RuntimeError:
        chat_ids = asyncio.get_event_loop().run_until_complete(get_all_ids())
        for cid in chat_ids:
            try:
                bot.send_message(cid, text)
            except Exception:
                pass