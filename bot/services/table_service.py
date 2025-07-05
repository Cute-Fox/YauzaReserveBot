from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.table_request import TableRequest

async def save_table(session: AsyncSession, **kwargs) -> TableRequest:
    obj = TableRequest(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
