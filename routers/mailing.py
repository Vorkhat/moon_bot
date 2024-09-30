from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from routers.start import menu_router
from utils.mailing import send_message_to_users

# Создаем маршруты
create_mailing = Router()
create_mailing_text = Router()
create_mailing_confirm = Router()

mailing_text = ""

@create_mailing.message(F.text.lower() == "создать рассылку")
async def create_mailing_router(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back_to_menu")

    await message.answer(
        text="Введите текст рассылки",
        reply_markup=builder.as_markup()
    )

@create_mailing_text.message(F.text)
async def create_mailing_text_router(message: Message):
    global mailing_text
    mailing_text = message.text

    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить", callback_data="confirm")
    builder.button(text="Назад", callback_data="back_to_start")

    await message.answer(
        text=f'Проверь текст рассылки, нажми подтвердить чтобы запустить:\n\n{mailing_text}',
        reply_markup=builder.as_markup()
    )

@create_mailing_confirm.callback_query(F.data)
async def create_mailing_confirm_router(callback: CallbackQuery):
    if callback.data == "confirm":
        await callback.message.answer(text="Рассылка успешно начата")
        await send_message_to_users(mailing_text)
    elif callback.data == "back_to_start":
        await create_mailing_router(callback.message)
    elif callback.data == "back_to_menu":
        await menu_router(callback.message)
