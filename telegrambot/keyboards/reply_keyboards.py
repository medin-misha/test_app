from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ReplaysKeyboards:
    def menu(self) -> ReplyKeyboardMarkup:
        line1 = [KeyboardButton(text="/createSpending"), KeyboardButton(text="/getSpendings")]
        line2 = [KeyboardButton(text="/deleteSpending"), KeyboardButton(text="updateSpending")]
        line3 = [KeyboardButton(text="я так мало зарабатываю....")]
        return ReplyKeyboardMarkup(keyboard=[line1, line2, line3], resize_keyboard=True)

    def state_clear(self):
        line1 = [KeyboardButton("я нажал что то не то")]
        return ReplyKeyboardMarkup(keyboards=[line1], resize_keyboard=True)