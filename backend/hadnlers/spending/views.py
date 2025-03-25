from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from core import db_helper, login, User, Spending
from .utils import (
    CreateXLSFile,
    create_spending,
    get_spendings,
    get_spending_by_id,
    put_spending,
    get_up_date_to_date_spendings,
)
from .schemes import (
    XLSSpendingScheme,
    CreateSpending,
    SpendingScheme,
    ReturnSpendingScheme,
)


router = APIRouter(prefix="/api/spending", tags=["spending"])
create_xls = CreateXLSFile()


@router.get("/{up_date:str}/{to_date:str}")
async def get_spendings_by_dates(
    up_date: date,
    to_date: date,
    session: AsyncSession = Depends(db_helper.get_session),
    user: User = Depends(login),
) -> Response:
    """
    Возвращает расходы пользователя за указанный период в виде XLS-файла.

    Args:
        up_date (date): Начальная дата периода.
        to_date (date): Конечная дата периода.
        session (AsyncSession): Сессия базы данных.
        user (User): Авторизованный пользователь.

    Returns:
        Response: XLS-файл с расходами за заданный период.
    """

    spendings = await get_up_date_to_date_spendings(
        session=session, user_id=user.id, up_date=up_date, to_date=to_date
    )
    if spendings is None:
        return
    xls_spendings = [
        XLSSpendingScheme(id=item.id, name=item.name, date=item.date, money=item.money)
        for item in spendings
    ]

    xls_file = await create_xls.create_table(spendings=xls_spendings)
    return Response(
        content=xls_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="spendings.xlsx"'},
    )


@router.post("/")
async def create_spending_view(
    data: SpendingScheme | List[SpendingScheme],
    user: User = Depends(login),
    session: AsyncSession = Depends(db_helper.get_session),
) -> ReturnSpendingScheme:
    """
    Создаёт одну или несколько записей о расходах для текущего пользователя.

    Args:
        data (SpendingScheme | List[SpendingScheme]): Данные о расходах.
        user (User): Авторизованный пользователь.
        session (AsyncSession): Сессия базы данных.

    Returns:
        Spending | List[Spending]: Созданная запись или список записей о расходах.
    """

    if isinstance(data, list):
        spendings: List[Spending] = [
            await create_spending(
                session=session,
                data=CreateSpending(
                    user_id=user.id, money=elem.money, name=elem.name, date=elem.date
                ),
            )
            for elem in data
        ]
        return spendings
    modification_data = CreateSpending(
        user_id=user.id, money=data.money, name=data.name, date=data.date
    )
    return await create_spending(session=session, data=modification_data)


@router.get("/")
async def get_spendings_view(
    session=Depends(db_helper.get_session),
) -> List[ReturnSpendingScheme]:
    """
    Возвращает список всех записей о расходах.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        List[Spending]: Список всех расходов.
    """

    return await get_spendings(session=session)


@router.put("/{id:int}")
async def put_spending_view(
    id: int,
    data: SpendingScheme,
    session: AsyncSession = Depends(db_helper.get_session),
    user: User = Depends(login),
) -> ReturnSpendingScheme:
    """
    Обновляет запись о расходе по указанному ID, если она принадлежит текущему пользователю.

    Args:
        id (int): Идентификатор расхода.
        data (SpendingScheme): Новые данные для обновления.
        session (AsyncSession): Сессия базы данных.
        user (User): Авторизованный пользователь.

    Returns:
        Spending: Обновлённая запись о расходе.

    Raises:
        HTTPException: Если запись не найдена или не принадлежит пользователю.
    """

    spending = await get_spending_by_id(session=session, id=id)
    if spending is not None and user.id == spending.user_id:
        await put_spending(id=id, session=session, new_data=data)
        return spending
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено!")


@router.delete("/{id:int}", status_code=204)
async def delete_spending(
    id: int,
    session: AsyncSession = Depends(db_helper.get_session),
    user: User = Depends(login),
) -> None:
    """
    Удаляет запись о расходе по указанному ID, если она принадлежит текущему пользователю.

    Args:
        id (int): Идентификатор расхода.
        session (AsyncSession): Сессия базы данных.
        user (User): Авторизованный пользователь.

    Raises:
        HTTPException: Если запись не найдена или не принадлежит пользователю.
    """
    spending = await get_spending_by_id(session=session, id=id)
    if spending is not None and user.id == spending.user_id:
        await session.delete(spending)
        await session.commit()
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено!")
