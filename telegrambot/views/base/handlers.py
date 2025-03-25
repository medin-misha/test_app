from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from keyboards import replays
from utils import registration

router = Router(name="base_router")


@router.message(CommandStart())
async def start_handlers(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    await registration(user_id=msg.chat.id)
    await msg.reply(
        text="<b>Привет!</b> Я бот, который поможет тебе <i>наконец-то</i> перестать покупать бесполезную дичь! 🛑\nЗаписывай все свои <u>расходы</u> в меня, и не забудь про оправдания, что тебе мало платят это же не ты транжиришь а тебе, недоплачивают. 💸\nСкоро ты будешь контролировать свой бюджет как профессионал! 🚀",
        reply_markup=replays.menu(),
    )
    await state.clear()


@router.message(F.text == "я так мало зарабатываю....")
async def whining_hadnler(msg: Message, state: FSMContext):
    await msg.bot.send_chat_action(action=ChatAction.TYPING, chat_id=msg.chat.id)
    await msg.reply(
        text="Какой ты бедненький, не бойся как нибуть прорвёмся:)",
        reply_markup=replays.menu(),
    )
