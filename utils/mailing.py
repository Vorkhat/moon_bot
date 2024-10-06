import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder
from prisma import Prisma
from config_reader import bot


async def get_user_ids(prisma: Prisma, offset: int = 0, limit: int = 100):
    users = await prisma.user.find_many(
        skip=offset,
        take=limit,
        where={"access": True}
    )
    return [user.tgUserId for user in users]


async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str, photo_id: str = '0'):
    offset = 0
    limit = 100
    builder = InlineKeyboardBuilder()
    builder.button(text=keyboard_text, url=keyboard_link)

    async with Prisma() as prisma:
        while True:
            user_ids = await get_user_ids(prisma, offset=offset, limit=limit)

            if not user_ids:
                break

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

                    await prisma.user.update(
                        where={"tgUserId": user_id},
                        data={"access": False}
                    )

                await asyncio.sleep(0.025)

            offset += limit
