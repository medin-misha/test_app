from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from typing import List
from core import User


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User)
    users: Result = await session.execute(stmt)
    return users.scalars().all()
