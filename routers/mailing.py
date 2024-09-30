from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.maiiling import send_message_to_users

create_mailing = Router()
create_mailing_text = Router()
create_mailing_confirm = Router()

mailing_text = ""

@create_mailing.callback_query(F.data == "mailling")
async def router(callback: types.CallbackQuery):
    await callback.message.answer("Введите текст рассылки")

@create_mailing_text.message(F.text)
async def router(message: Message):
    global mailing_text
    mailing_text = message.text

    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить", callback_data="confirm")
    builder.button(text="Menu", callback_data="menu")

    await message.answer(
        text=f'Проверь текст рассылки, нажми подтвердить чтобы запустить:\n\n{mailing_text}',
        reply_markup=builder.as_markup()
    )

@create_mailing_confirm.callback_query(F.data)
async def router(callback: types.CallbackQuery):
    if callback.data == "confirm":

        await send_message_to_users(mailing_text)
        await callback.message.answer(text="Рассылка успешно начата")
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text="Создать рассылку", callback_data="mailling")

        await callback.message.answer(
            text="Вы вернулись в меню",
            reply_markup=builder.as_markup()
        )
