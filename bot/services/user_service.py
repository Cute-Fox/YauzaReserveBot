from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User

async def get_user(session: AsyncSession, tg_id: int) -> User | None:
   stmt = select(User).where(User.tg_id == tg_id)
   result = await session.execute(stmt)
   return result.scalar_one_or_none()

async def save_user(session: AsyncSession, tg_id: int, name: str) -> User:
    user = User(tg_id=tg_id, name=name)
    session.add(user)
    await session.commit()
    return user

async def set_admin(session: AsyncSession, tg_id: int, value: bool) -> None:
    stmt = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(is_admin=value)
    )
    await session.execute(stmt)
    await session.commit()

async def get_admin_ids(session) -> list[int]:
    stmt = select(User.tg_id).where(User.is_admin.is_(True))
    res  = await session.execute(stmt)
    return [row[0] for row in res]

async def ensure_user(session: AsyncSession, tg_user) -> User:
    user = await get_user(session, tg_user.id)
    if user is None:
        user = await save_user(session, tg_user.id, tg_user.full_name)
    return user