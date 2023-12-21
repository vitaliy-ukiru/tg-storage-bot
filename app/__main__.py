import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bot.handlers import dialogs, users
from app.bot.middlewares import UserMiddleware
from app.bot.middlewares import FileUploaderMiddleware
from app.bot.middlewares.proxy_middlewares import (CategoryProxyMiddleware,
                                                   FileProxyMiddleware)
from app.common.config import Loader
from app.infrastructure.db.config import to_dsn
from app.infrastructure.db.repo.category import CategoryStorage
from app.infrastructure.db.repo.file import FileStorage
from app.infrastructure.db.repo.user import UserStorage
from app.core.domain.services.category import CategoryService
from app.core.domain.services.file import FileService
from app.core.domain.services.user import UserService


async def main():
    env = Env()
    env.read_env()

    loader = Loader.read(env=env)
    cfg = loader.load()
    engine = create_async_engine(to_dsn(cfg.db), echo=cfg.is_debug)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    if cfg.env == "dev":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info(f"env is {cfg.env!r}")

    storage = MemoryStorage()
    bot = Bot(token=cfg.tg_bot.token)
    dp = Dispatcher(storage=storage)

    user_repo = UserStorage(session_maker)
    category_repo = CategoryStorage(session_maker)
    file_repo = FileStorage(session_maker)

    user_service = UserService(user_repo)
    category_service = CategoryService(category_repo, file_repo)
    file_service = FileService(file_repo, category_service)

    dp.update.middleware(UserMiddleware(user_service))
    dp.update.middleware(FileProxyMiddleware(file_service))
    dp.update.middleware(CategoryProxyMiddleware(category_service))
    dp.message.middleware(FileUploaderMiddleware(file_service))

    users.setup(dp)
    dialogs.setup(dp)

    # dp.message.register(start, CommandStart())
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
