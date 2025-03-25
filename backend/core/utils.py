from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models.user import User


async def get_user_by_chat_id(session: AsyncSession, chat_id: str) -> User | None:
    user_stmt = select(User).where(User.chat_id == chat_id)
    user: Result = await session.execute(user_stmt)
    return user.scalar()
