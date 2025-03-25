from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = f"postgresql+asyncpg://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}"
    currencylayer_key: str = f"{os.getenv("currencylayer_key")}"
    quotes_uah_usd: float = 41.787683

settings = Settings()
