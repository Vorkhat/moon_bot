import asyncio

from main import bot
from utils.db import get_user_ids


async def send_message_to_users(message_text: str):
    user_ids = await get_user_ids()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)
        except Exception as error:
            print(error)
        await asyncio.sleep(0.2)