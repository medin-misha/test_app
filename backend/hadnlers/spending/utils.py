from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from openpyxl import Workbook
import aiohttp
import io
from datetime import date
from typing import List, Any
from core import settings, Spending
from .schemes import CreateSpending, SpendingScheme


class CreateXLSFile:
    async def uah_in_usd(self, uah: float) -> float:
        async with aiohttp.ClientSession() as session:
            url: str = f"http://apilayer.net/api/live?access_key={settings.currencylayer_key}&currencies=UAH&source=USD&format=1"
            async with session.get(url) as response:
                response_json: dict = await response.json()
                if response_json.get("success"):
                    usd_uah = response_json.get("quotes").get("USDUAH")
                    settings.quotes_uah_usd = usd_uah
                    return round(uah / usd_uah, 2)
                return round(uah / settings.quotes_uah_usd, 2)

    async def create_table(self, spendings: List[dict]) -> io.BytesIO:
        columns: List[str] = ["id", "name", "money(uah)", "money(usd)", "date"]
        workbook = Workbook()
        workspace = workbook.active
        workspace.append(columns)
        for spending in spendings:
            row: List[Any] = [
                spending.id,
                spending.name,
                spending.money,
                await self.uah_in_usd(spending.money),
                spending.date,
            ]
            workspace.append(row)

        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)
        return output


async def create_spending(session: AsyncSession, data: CreateSpending):
    spending = Spending(**data.model_dump())
    session.add(spending)
    await session.commit()
    await session.refresh(spending)
    return spending


async def get_spendings(session: AsyncSession) -> List[Spending]:
    stmt = select(Spending)
    spendings: Result = await session.execute(stmt)
    return spendings.scalars().all()


async def get_spending_by_id(session: AsyncSession, id: int) -> Spending | None:
    stmt = select(Spending).where(Spending.id == id)
    spending: Result = await session.execute(stmt)
    return spending.scalar()


async def put_spending(
    session: AsyncSession, id: int, new_data: SpendingScheme
) -> Spending | None:
    spending = await get_spending_by_id(session=session, id=id)
    if spending is None:
        return None
    for name, value in new_data.model_dump().items():
        setattr(spending, name, value)
    await session.commit()
    return spending


async def get_up_date_to_date_spendings(
    user_id: int, up_date: date, to_date: date, session: AsyncSession
) -> List[Spending] | None:
    stmt = select(Spending).where(
        Spending.user_id == user_id, up_date <= Spending.date, Spending.date <= to_date
    )
    spendings: Result = await session.execute(stmt)
    return spendings.scalars().all() or None
