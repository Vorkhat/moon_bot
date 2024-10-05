import asyncio
from typing import Any, Dict, Callable, Awaitable

from aiogram.types import Message

from config_reader import config, bot
from aiogram import Dispatcher, BaseMiddleware

from routers.menu import menu
from routers.mailing import create_mailing


class AdminAccessMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        if event.from_user.id in config.admins or event.text in ['/start']:
            return await handler(event, data)
        else:
            return ...


async def main():
    dp = Dispatcher()

    dp.message.middleware.register(AdminAccessMiddleware())
    dp.include_routers(
        menu,
        create_mailing)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
