import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.middlewares import UserMiddleware
from bot.middlewares.proxy_middlewares import (CategoryProxyMiddleware,
                                               FileProxyMiddleware)
from bot.middlewares.file_uploader import FileUploaderMiddleware
from bot.handlers.dialogs.setup import router as get_dialog_router
from bot.handlers.users.files.upload import router as upload_router
from core.adapters.storage.category import CategoryGateway
from core.adapters.storage.database import DSN
from core.adapters.storage.file import FileGateway
from core.adapters.storage.user import UserGateway
from core.domain.services.category import CategoryService
from core.domain.services.file import FileService
from core.domain.services.user import UserService

API_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    engine = create_async_engine(DSN, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=storage)

    user_repo = UserGateway(session_maker)
    category_repo = CategoryGateway(session_maker)
    file_repo = FileGateway(session_maker)

    user_service = UserService(user_repo)
    category_service = CategoryService(category_repo)
    file_service = FileService(file_repo, category_service)

    dp.update.middleware(UserMiddleware(user_service))
    upload_router.message.middleware(FileUploaderMiddleware(file_service))
    dp.update.middleware(FileProxyMiddleware(file_service))
    dp.update.middleware(CategoryProxyMiddleware(category_service))
    dp.include_router(get_dialog_router())

    # dp.message.register(start, CommandStart())
    setup_dialogs(dp)
    dp.include_router(upload_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
