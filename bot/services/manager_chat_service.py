from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.manager_chat import ManagerChat

async def add_chat(session: AsyncSession, chat_id: int, title: str | None):
    stmt = insert(ManagerChat).values(chat_id=chat_id, title=title).on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()

async def remove_chat(session: AsyncSession, chat_id: int):
    await session.execute(delete(ManagerChat).where(ManagerChat.chat_id == chat_id))
    await session.commit()

async def all_chat_ids(session: AsyncSession) -> list[int]:
    res = await session.execute(select(ManagerChat.chat_id))
    return [row[0] for row in res]
