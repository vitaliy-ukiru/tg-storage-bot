import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bot.handlers.dialogs.setup import router as get_dialog_router
from app.bot.handlers.users.files.list import router as list_router
from app.bot.handlers.users.files.upload import router as upload_router
from app.bot.middlewares import UserMiddleware
from app.bot.middlewares import FileUploaderMiddleware
from app.bot.middlewares.proxy_middlewares import (CategoryProxyMiddleware,
                                                   FileProxyMiddleware)
from app.infrastructure.db import DSN
from app.infrastructure.db.repo.category import CategoryStorage
from app.infrastructure.db.repo.file import FileStorage
from app.infrastructure.db.repo.user import UserStorage
from app.core.domain.services.category import CategoryService
from app.core.domain.services.file import FileService
from app.core.domain.services.user import UserService

API_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    engine = create_async_engine(DSN, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=storage)

    user_repo = UserStorage(session_maker)
    category_repo = CategoryStorage(session_maker)
    file_repo = FileStorage(session_maker)

    user_service = UserService(user_repo)
    category_service = CategoryService(category_repo, file_repo)
    file_service = FileService(file_repo, category_service)

    dp.update.middleware(UserMiddleware(user_service))
    upload_router.message.middleware(FileUploaderMiddleware(file_service))
    dp.update.middleware(FileProxyMiddleware(file_service))
    dp.update.middleware(CategoryProxyMiddleware(category_service))

    dp.include_routers(
        upload_router,
        list_router,
    )
    dp.include_router(get_dialog_router())

    # dp.message.register(start, CommandStart())
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
