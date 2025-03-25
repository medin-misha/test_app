from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from keyboards import replays
from utils import (
    create_spending,
    delete_spendings,
    get_spending_by_id,
    put_spending_by_id,
)
from .states import CreateSpending, GetSpendings, DeleteSpendings
from .utils import valid_date, format_date, send_monthly_report

router = Router(name="spending_router")



@router.message(Command("createSpending"), StateFilter("*"))
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


@router.message(Command("updateSpending"), StateFilter("*"))
async def update_spending_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    await send_monthly_report(msg=msg)
    await msg.reply(text="Скинь ID той записи которую ты хочешь поменять")
    await state.set_state(CreateSpending.id)


@router.message(Command("getSpendings"), StateFilter("*"))
async def get_spendings_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    await msg.reply(text="Хорошо. От какой даты мне смотреть? (в формате YYYY.MM.DD)")
    await state.set_state(GetSpendings.up_date)


@router.message(Command("deleteSpending"), StateFilter("*"))
async def delete_spendings_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    await send_monthly_report(msg=msg)
    await msg.reply(text="Для удаления записи мне нужен её ID")
    await state.set_state(DeleteSpendings.get_id)

# create spending states
@router.message(CreateSpending.name, F.text)
async def get_name_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    name: str = msg.text
    await state.update_data(name=name)
    await msg.reply(text="Пожалуйста, введите дату (в формате YYYY.MM.DD): ")
    await state.set_state(CreateSpending.date)


@router.message(CreateSpending.date, F.text)
async def get_date_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    if valid_date(date=msg.text):
        await msg.reply(text="Отлично, впиши количество потраченого золота")
        await state.update_data(date=format_date(date=msg.text))
        await state.set_state(CreateSpending.money)
    else:
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
            text=f"💰 *Новая трата добавлена!*\n\n📅 *Дата:* {spending.get('date')}\n💵 *Сумма:* {spending.get('money')} UAH\n🛒 *имя:* {spending.get('name')}\n🆔 *ID:* {spending.get('id')}",
            reply_markup=replays.menu(),
        )
        await state.clear()
    else:
        await msg.reply(text="ты скинул что то не то, попробуй ещё раз")


# Get Spendings
@router.message(GetSpendings.up_date, F.text)
async def get_up_date_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    if valid_date(date=msg.text):
        await msg.reply(text="Теперь до какой даты? (в формате YYYY.MM.DD)")
        await state.update_data(up_date=format_date(date=msg.text))
        await state.set_state(GetSpendings.to_date)
    else:
        await msg.reply(text="ты скинул что то не то, попробуй ещё раз.")


@router.message(GetSpendings.to_date, F.text)
async def get_to_date_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    if valid_date(date=msg.text):
        await msg.reply(text="Подожди...")
        await state.update_data(to_date=format_date(date=msg.text))
        data: dict = await state.get_data()
        await send_monthly_report(
            msg=msg, up_date=data.get("up_date"), to_date=data.get("to_date")
        )
        await msg.reply(text="Вот отчёт.", reply_markup=replays.menu())
        await state.clear()
    else:
        await msg.reply(text="ты скинул что то не то, попробуй ещё раз.")


# depelete spending
@router.message(DeleteSpendings.get_id, F.text)
async def get_id_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    if not msg.text.isdigit():
        await msg.reply(text="Ты ввёл что то не то.", reply_markup=replays.menu())
    else:
        response = await delete_spendings(user_id=msg.chat.id, spending_id=msg.text)
        await msg.reply(
            text="запись успешно удалена." if response else "такая запись не найдена.",
            reply_markup=replays.menu(),
        )
        await state.clear()


# update handlers
@router.message(CreateSpending.id, F.text)
async def update_get_spending_id_handler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    if not msg.text.isdigit():
        await msg.reply(text="Ты ввёл что то не то.", reply_markup=replays.menu())
    else:
        await state.update_data(id=msg.text)
        spending = await get_spending_by_id(user_id=msg.chat.id, spending_id=msg.text)
        await state.update_data(old_spending=spending)
        await msg.reply(
            text=f"💰 *трата*\n\n📅 *Дата:* {spending.get('date')}\n💵 *Сумма:* {spending.get('money')} UAH\n🛒 *имя:* {spending.get('name')}\n🆔 *ID:* {spending.get('id')}",
            reply_markup=replays.menu(),
        )
        await msg.reply(
            text="Теперь через пробел введи новые значения имени и цены. \nесли нужно заменить что то одно введи на его месте `-`.\nнапример: мороженное 20 или - 20 или мороженное -"
        )
        await state.set_state(CreateSpending.update)


@router.message(CreateSpending.update, F.text)
async def update_get_new_values(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    new_values = msg.text.split()
    if len(new_values) == 2:
        state_data: dict = await state.get_data()
        updated_spending_data: dict = {
            "name": state_data.get("old_spending").get("name")
            if new_values[0] == "-"
            else new_values[0],
            "money": state_data.get("old_spending").get("money")
            if new_values[1] == "-" or not new_values[1].isdigit()
            else new_values[1],
            "date": state_data.get("old_spending").get("date"),
        }
        response = await put_spending_by_id(
            user_id=msg.chat.id,
            spending_id=state_data.get("id"),
            new_spending=updated_spending_data,
        )
        if response.get("id"):
            await msg.reply(
                text=f"💰 *Новая трата добавлена!*\n\n📅 *Дата:* {response.get('date')}\n💵 *Сумма:* {response.get('money')} UAH\n🛒 *имя:* {response.get('name')}\n🆔 *ID:* {response.get('id')}",
                reply_markup=replays.menu(),
            )
            await state.clear()
    else:
        await msg.reply(text="Ты ввёл что то не то.", reply_markup=replays.menu())


# error handler
@router.message()
async def error_get_id_view(msg: Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.TYPING)
    await msg.reply(
        text="Слушай, когда ты мне отправляешь <i>подобную штуку</i> у меня в место текста высвечиваеться <code>None</code>. Я не вдупляю стикеры, смайлы, картинки и так далее. <b>Скинь текстом.</b>",
    )
