import asyncio
import logging
from argparse import ArgumentParser

from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.setup import BotModule
from app.common.config import Config
from app.core.domain.services.category import CategoryService
from app.core.domain.services.file import FileService
from app.core.domain.services.user import UserService
from app.infrastructure.adapters.category_rater import CategoryRaterAdapter
from app.infrastructure.db import connect
from app.infrastructure.db.repo.category import CategoryStorage
from app.infrastructure.db.repo.file import FileStorage
from app.infrastructure.db.repo.user import UserStorage


async def main():
    parser = ArgumentParser(description="Telegram bot for stores files")
    parser.add_argument(
        "--config", help="path to config file",
        default="configs/local.yaml"
    )
    args = parser.parse_args()

    cfg = Config(_yaml_file=args.config)

    engine = connect.connect_db(cfg)
    session_maker = connect.new_session_maker(engine)

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
        cfg.bot,
        user_service,
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
