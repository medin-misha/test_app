from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str = f"postgresql+asyncpg://{os.getenv('postgres_user')}:{os.getenv('postgres_password')}@{os.getenv('postgres_host')}"


settings = Settings()
print(settings.database_url)
