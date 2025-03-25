from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from .database import db_helper
from .models.user import User
from .utils import get_user_by_chat_id

sucurity = HTTPBasic()


async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(sucurity)],
    session: AsyncSession = Depends(db_helper.get_session),
) -> User:
    # credentials.password is chat_id
    chat_id: str = credentials.password
    user = await get_user_by_chat_id(session=session, chat_id=chat_id)
    if user is None:
        raise HTTPException(
            status=status.HTTP_401_UNAUTHORIZED, detail="user not found!"
        )
    return user
