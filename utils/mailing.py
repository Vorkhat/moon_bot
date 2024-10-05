import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import bot
from utils.db import get_user_ids


async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str, photo_id: int):
    user_ids = await get_user_ids()

    for user_id in user_ids:
        try:
            builder = InlineKeyboardBuilder()
            builder.button(text=keyboard_text, url=keyboard_link)
            await bot.send_photo(
                chat_id=user_id,
                photo=photo_id,
                caption=message_text,
                reply_markup=builder.as_markup()
            )
        except Exception as error:
            print(error)
        await asyncio.sleep(0.25)
