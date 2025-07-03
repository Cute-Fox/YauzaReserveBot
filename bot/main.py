from telebot import TeleBot
from bot.config import get_settings
from bot.handlers import register as register_handlers
from bot.middlewares import register as register_middlewares

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.async_app import loop      # ← наш общий loop

settings = get_settings()
bot = TeleBot(settings.bot_token, parse_mode="HTML")

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)


engine = create_async_engine(DATABASE_URL, echo=settings.echo_sql)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def run() -> None:
    register_middlewares(bot, SessionLocal)
    register_handlers(bot, SessionLocal)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    run()
