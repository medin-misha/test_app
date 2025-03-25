from aiogram.types import Message
from datetime import timedelta, datetime

from utils import get_spendings


def valid_date(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y.%m.%d")
        return True
    except ValueError:
        return False


def format_date(date: str) -> bool:
    parts = date.split(".")
    return f"{parts[0]}-{parts[1]}-{parts[2]}"


def generate_dates():
    today = datetime.today().date()
    past_date = today - timedelta(days=15)
    future_date = today + timedelta(days=15)
    return past_date, future_date


async def send_monthly_report(
    msg: Message, up_date: str = generate_dates()[0], to_date: str = generate_dates()[1]
) -> None:
    await msg.reply_document(
        document=await get_spendings(
            user_id=msg.chat.id,
            up_date=up_date,
            to_date=to_date,
        )
    )
