from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.table_request   import TableRequest
from bot.models.banquet_request import BanquetRequest


async def all_table_bookings(
    session: AsyncSession, *, upcoming: bool = False
) -> list[TableRequest]:
    stmt = select(TableRequest).order_by(TableRequest.reserve_date, TableRequest.reserve_time)
    if upcoming:
        stmt = stmt.where(TableRequest.reserve_date >= date.today())
    res = await session.execute(stmt)
    return res.scalars().all()


async def all_banquets(
    session: AsyncSession, *, upcoming: bool = False
) -> list[BanquetRequest]:
    stmt = select(BanquetRequest).order_by(BanquetRequest.banquet_date, BanquetRequest.banquet_time)
    if upcoming:
        stmt = stmt.where(BanquetRequest.banquet_date >= date.today())
    res = await session.execute(stmt)
    return res.scalars().all()


async def stats(session: AsyncSession) -> dict[str, int]:
    today = date.today()

    banquet_cnt = await session.scalar(
        select(func.count()).select_from(BanquetRequest).where(BanquetRequest.banquet_date >= today)
    )
    table_cnt = await session.scalar(
        select(func.count()).select_from(TableRequest).where(TableRequest.reserve_date >= today)
    )
    banquet_sum = await session.scalar(
        select(func.sum(BanquetRequest.guests)).where(BanquetRequest.banquet_date >= today)
    )
    table_sum = await session.scalar(
        select(func.sum(TableRequest.guests)).where(TableRequest.reserve_date >= today)
    )
    return {
        "banquet_cnt": banquet_cnt or 0,
        "table_cnt":   table_cnt   or 0,
        "banquet_sum": banquet_sum or 0,
        "table_sum":   table_sum   or 0,
    }
