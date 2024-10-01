from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from routers.start import menu_router
from utils.mailing import send_message_to_users

create_mailing = Router()

class MailingStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_button_text = State()
    waiting_for_keyboard_link = State()
    confirm = State()

@create_mailing.message(F.text.lower() == "создать рассылку")
async def create_mailing_router(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back_to_menu")

    await message.answer(
        text="Введите текст рассылки",
        reply_markup=builder.as_markup()
    )
    await state.set_state(MailingStates.waiting_for_text)

@create_mailing.message(MailingStates.waiting_for_text)
async def handle_mailing_text(message: Message, state: FSMContext):
    await state.update_data(mailing_text=message.text)

    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back_to_text")

    await message.answer(
        text="Теперь введите текст кнопки:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(MailingStates.waiting_for_button_text)

@create_mailing.message(MailingStates.waiting_for_button_text)
async def handle_button_text(message: Message, state: FSMContext):
    await state.update_data(button_text=message.text)

    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="back_to_button_text")

    await message.answer(
        text="Теперь укажите ссылку для кнопки (например, URL):",
        reply_markup=builder.as_markup()
    )
    await state.set_state(MailingStates.waiting_for_keyboard_link)

@create_mailing.message(MailingStates.waiting_for_keyboard_link)
async def handle_keyboard_link(message: Message, state: FSMContext):
    await state.update_data(keyboard_link=message.text)

    data = await state.get_data()
    mailing_text = data['mailing_text']
    button_text = data['button_text']
    keyboard_link = data['keyboard_link']

    buttons = [
        [
            types.InlineKeyboardButton(
                text=button_text,
                url=keyboard_link
            )
        ],
        [
            types.InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
            types.InlineKeyboardButton(text="Назад к ссылке", callback_data="back_to_link")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        text=f'Проверь текст рассылки и нажми "Подтвердить", чтобы запустить:\n\n{mailing_text}',
        reply_markup=keyboard
    )
    await state.set_state(MailingStates.confirm)

@create_mailing.callback_query(F.data)
async def handle_callbacks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mailing_text = data.get('mailing_text', '')
    button_text = data.get('button_text', '')
    keyboard_link = data.get('keyboard_link', '')

    if callback.data == "confirm":
        await callback.message.answer("Рассылка успешно начата")
        await send_message_to_users(mailing_text, button_text, keyboard_link)
        await state.clear()

    elif callback.data == "back_to_text":
        await state.set_state(MailingStates.waiting_for_text)
        builder = InlineKeyboardBuilder()
        builder.button(text="Назад", callback_data="back_to_menu")
        await callback.message.answer(
            text="Введите текст рассылки:",
            reply_markup=builder.as_markup()
        )

    elif callback.data == "back_to_button_text":
        await state.set_state(MailingStates.waiting_for_button_text)
        builder = InlineKeyboardBuilder()
        builder.button(text="Назад", callback_data="back_to_text")
        await callback.message.answer(
            text="Введите текст кнопки:",
            reply_markup=builder.as_markup()
        )

    elif callback.data == "back_to_link":
        await state.set_state(MailingStates.waiting_for_keyboard_link)
        builder = InlineKeyboardBuilder()
        builder.button(text="Назад", callback_data="back_to_button_text")
        await callback.message.answer(
            text="Введите ссылку на клавиатуру:",
            reply_markup=builder.as_markup()
        )

    elif callback.data == "back_to_menu":
        await state.clear()
        await menu_router(callback.message)
