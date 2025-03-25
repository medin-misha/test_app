from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from keyboards import replays
from utils import create_spending
from .states import CreateSpending

router = Router(name="spending_router")


# create spending states
@router.message(Command("createSpending"))
async def create_spending_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)

    msg_split: list = msg.text.split()
    if len(msg_split) == 4:
        data: dict = {"date": msg_split[1], "money": msg_split[2], "name": msg_split[3]}
        spending = await create_spending(user_id=msg.chat.id, data=data)
        await msg.reply(
            text=f"Создал:\ndate: {spending.get('date')}\nmoney: {spending.get('money')}\nname: {spending.get('name')}"
        )
    else:
        await msg.reply(text="Пожалуйста, введите название вашей траты:")
        await state.set_state(CreateSpending.name)


@router.message(CreateSpending.name, F.text)
async def get_name_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    name: str = msg.text
    await state.update_data(name=name)
    await msg.reply(text="Пожалуйста, введите дату (в формате YYYY.MM.DD): ")
    await state.set_state(CreateSpending.date)
    print("Состояние изменено на CreateSpending.date")


@router.message(CreateSpending.date, F.text)
async def get_date_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    try:
        datetime.strptime(msg.text, "%Y.%m.%d")
        parts = msg.text.split(".")
        correct_format_date: str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        await msg.reply(text="Отлично, впиши количество потраченого золота")
        await state.update_data(date=correct_format_date)
        await state.set_state(CreateSpending.money)
    except ValueError:
        await msg.reply(text="ты скинул что то не то, попробуй ещё раз.")


@router.message(CreateSpending.money, F.text)
async def get_money_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    money: str = msg.text
    if msg.text.isdigit():
        states_data: dict = await state.get_data()
        data: dict = {
            "date": states_data.get("date"),
            "name": states_data.get("name"),
            "money": float(money),
        }
        spending: dict = await create_spending(user_id=str(msg.chat.id), data=data)

        await msg.reply(
            text=f"Создал:\ndate: {spending.get('date')}\nmoney: {spending.get('money')}\nname: {spending.get('name')}"
        )
        await state.clear()
    else:
        await msg.reply(text="ты скинул что то не то, попробуй ещё раз")


# error handler
@router.message(CreateSpending.name, CreateSpending.money, CreateSpending.date)
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
    )
