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
