from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    postgres_host: str = Field("db", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("yauza", env="POSTGRES_DB")
    postgres_user: str = Field("yauza", env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    echo_sql: bool = Field(False, env="ECHO_SQL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
