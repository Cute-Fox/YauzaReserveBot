from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    bot_token: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
