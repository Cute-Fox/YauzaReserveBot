from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.banquet_request import BanquetRequest

async def save_banquet(session: AsyncSession, **kwargs) -> BanquetRequest:
    obj = BanquetRequest(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
