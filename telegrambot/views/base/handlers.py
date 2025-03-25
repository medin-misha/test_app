from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
router = Router(name="base_router")


@router.message(CommandStart)
async def start_handlers(msg: Message):
    await msg.reply(text="хорошая новость: бот работает.")
