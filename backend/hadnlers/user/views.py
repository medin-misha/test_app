from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core import User, db_helper, get_user_by_chat_id, login
from .schemes import UserScheme, ReturnUser
from .utils import get_users

router = APIRouter(prefix="/api/users")


@router.post("/")
async def create_user_view(
    data: UserScheme, session: AsyncSession = Depends(db_helper.get_session)
) -> ReturnUser:
    """
    Эта функция поможет вам создать пользователя. Всё очень просто: отправьте в теле запроса chat_id.
    В ответе вы получите id и chat_id созданного пользователя. Таким образом, вы аутентифицируетесь в системе.
    """
    user = await get_user_by_chat_id(session=session, chat_id=data.chat_id)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Что то пошло не так!"
        )
    new_user = User(**data.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/")
async def get_users_list_view(
    session: AsyncSession = Depends(db_helper.get_session),
) -> List[ReturnUser]:
    """
    Эта функция поможет вам посмотреть всех юзеров и их id в списке.
    """
    return await get_users(session=session)
