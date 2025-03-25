from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.settings import settings


class DBHelper():
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url=url)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_maker() as session:
            yield session
            await session.close()


db_helper = DBHelper(url=settings.database_url)