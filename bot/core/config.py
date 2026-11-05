from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    
    # За замовчуванням SQLite, або передається PostgreSQL через docker-compose
    DATABASE_URL: str = "sqlite+aiosqlite:///./bot.db"
    DB_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
