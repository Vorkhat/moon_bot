from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

start = Router()
menu = Router()

@start.message(Command('start'))
async def start_router(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Создать рассылку")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Выберите команду", reply_markup=keyboard)

@menu.message(F.text.lower() == "menu")
async def menu_router(message: types.Message):
    await message.answer(
        text="Вы вернулись в главное меню",
    )