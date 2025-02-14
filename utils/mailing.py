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


async def send_message(user_id: int, message_text: str, builder, photo_id: str, prisma: Prisma):
    try:
        await bot.send_photo(
            chat_id=user_id,
            photo=photo_id,
            caption=message_text,
            reply_markup=builder.as_markup()
        )
        print(f"Сообщение отправлено пользователю {user_id}")
    except Exception as error:
        print(f"Ошибка при отправке пользователю {user_id}: {error}")
        await prisma.user.update(
            where={"tgUserId": user_id},
            data={"access": False}
        )


async def send_message_to_users(message_text: str, keyboard_text: str, keyboard_link: str, photo_id: str = '0'):
    offset = 0
    limit = 100
    batch_size = 25

    builder = InlineKeyboardBuilder()
    builder.button(text=keyboard_text, url=keyboard_link)

    async with Prisma() as prisma:
        while True:
            user_ids = await get_user_ids(prisma, offset=offset, limit=limit)
            if not user_ids:
                break

            tasks = []
            for user_id in user_ids:
                tasks.append(send_message(user_id, message_text, builder, photo_id, prisma))

                if len(tasks) >= batch_size:
                    await asyncio.gather(*tasks)
                    tasks = []
                    await asyncio.sleep(1)

            if tasks:
                await asyncio.gather(*tasks)

            offset += limit
