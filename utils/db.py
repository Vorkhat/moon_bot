from prisma import Prisma

async def get_user_ids():
    prisma = Prisma()

    await prisma.connect()

    try:
        users = await prisma.user.find_many()
        user_ids = [user.tgUserId for user in users]
        return [1311888287]
    finally:
        await prisma.disconnect()