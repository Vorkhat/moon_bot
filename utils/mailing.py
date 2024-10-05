import asyncio

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
from db import get_user_ids

bot = Bot(token=config.bot_token.get_secret_value())

async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str):
    user_ids = await get_user_ids()

    for user_id in user_ids:
        try:
            builder = InlineKeyboardBuilder()
            builder.button(text=keyboard_text, url=keyboard_link)
            await bot.send_message(user_id, message_text, reply_markup=builder.as_markup())
        except Exception as error:
            print(error)
        await asyncio.sleep(0.25)