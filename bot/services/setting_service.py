from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.setting import Setting


async def get(session: AsyncSession, key: str) -> str | None:
    stmt = select(Setting.value).where(Setting.key == key)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def set_(session: AsyncSession, key: str, value: str) -> None:
    exists = await get(session, key)
    if exists is None:
        stmt = insert(Setting).values(key=key, value=value)
    else:
        stmt = update(Setting).where(Setting.key == key).values(value=value)
    await session.execute(stmt)
    await session.commit()
