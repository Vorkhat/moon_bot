import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder
from prisma import Prisma
from config_reader import bot

MAX_MESSAGES_PER_SECOND = 25


async def get_user_ids(prisma: Prisma, offset: int = 0, limit: int = 100):
    users = await prisma.user.find_many(
        skip=offset,
        take=limit,
        where={"access": True}
    )
    return [user.tgUserId for user in users]


async def send_message(user_id, message_text, keyboard, photo_id, prisma, semaphore):
    async with semaphore:
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo_id,
                caption=message_text,
                reply_markup=keyboard
            )
        except Exception:
            await prisma.user.update(
                where={"tgUserId": user_id},
                data={"access": False}
            )


async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str, photo_id: str = '0'):
    offset = 0
    limit = 100
    semaphore = asyncio.Semaphore(MAX_MESSAGES_PER_SECOND)

    builder = InlineKeyboardBuilder()
    builder.button(text=keyboard_text, url=keyboard_link)
    keyboard = builder.as_markup()

    async with Prisma() as prisma:
        while True:
            user_ids = await get_user_ids(prisma, offset=offset, limit=limit)
            if not user_ids:
                break

            tasks = [send_message(user_id, message_text, keyboard, photo_id, prisma, semaphore) for user_id in user_ids]
            await asyncio.gather(*tasks)

            offset += limit
            await asyncio.sleep(1)  # Ограничение на уровень пакетов пользователей
