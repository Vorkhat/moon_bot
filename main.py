import asyncio
from typing import Any, Dict, Callable, Awaitable

from aiogram.types import Message

from config_reader import config
from aiogram import Bot, Dispatcher, BaseMiddleware

from routers.start import start, menu
from routers.mailing import create_mailing

bot = Bot(token=config.bot_token.get_secret_value())

class AdminAccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in config.admins:
            return
        return await handler(event, data)

async def main():
    dp = Dispatcher()

    dp.message.middleware.register(AdminAccessMiddleware())
    dp.include_routers(
        start, menu,
        create_mailing)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
