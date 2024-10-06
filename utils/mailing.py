import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import bot
from utils.db import get_user_ids


async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str, photo_id: str = '0'):
    user_ids = await get_user_ids()
    builder = InlineKeyboardBuilder()
    builder.button(text=keyboard_text, url=keyboard_link)

    await bot.send_photo(
        chat_id=1311888287,
        photo=photo_id,
        caption=message_text + f"\nКоличество пользователей: {len(user_ids)}",
        reply_markup=builder.as_markup()
    )

    for user_id in user_ids:
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo_id,
                caption=message_text,
                reply_markup=builder.as_markup()
            )
        except Exception as error:
            print(f"Сообщение пользователю: {user_id} - не смог отправить, ошибка: {error}")
        await asyncio.sleep(0.025)
