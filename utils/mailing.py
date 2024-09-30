import asyncio

from aiogram import Bot

from config_reader import config
from utils.db import get_user_ids

bot = Bot(token=config.bot_token.get_secret_value())

async def send_message_to_users(message_text: str):
    user_ids = await get_user_ids()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)
        except Exception as error:
            print(error)
        await asyncio.sleep(0.2)