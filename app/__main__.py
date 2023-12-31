import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.bot.setup import BotModule
from app.common.config import Loader
from app.core.domain.services.category import CategoryService, CategoryRater
from app.core.domain.services.file import FileService
from app.core.domain.services.user import UserService
from app.infrastructure.adapters.category_rater import CategoryRaterAdapter
from app.infrastructure.db.config import to_dsn
from app.infrastructure.db.repo.category import CategoryStorage
from app.infrastructure.db.repo.file import FileStorage
from app.infrastructure.db.repo.user import UserStorage


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

    user_repo = UserStorage(session_maker)
    category_repo = CategoryStorage(session_maker)
    file_repo = FileStorage(session_maker)

    user_service = UserService(user_repo)
    category_rater = CategoryRaterAdapter(file_repo)
    category_service = CategoryService(category_repo, category_rater)
    file_service = FileService(file_repo, category_service)

    tg_bot = BotModule(
        cfg.tg_bot, user_service,
        category_service,
        file_service,
        MemoryStorage(),
    )

    await tg_bot.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("shutdown")
