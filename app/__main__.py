import asyncio
import logging
from argparse import ArgumentParser

from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.builder import BotBuilder
from app.common.config import Config
from app.core.domain.services.category import CategoryService
from app.core.domain.services.file import FileService
from app.core.domain.services.user import UserService
from app.infrastructure.adapters.locale_provider import build_locale_provider
from app.infrastructure.db import connect
from app.infrastructure.db.repo.category import CategoryStorageGateway
from app.infrastructure.db.repo.file import FileStorageGateway, FileCategoryUsageRater
from app.infrastructure.db.repo.user import UserStorage


async def main():
    parser = ArgumentParser(description="Telegram bot for stores files")
    parser.add_argument(
        "--config", help="path to config file",
        default="configs/app.yaml"
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

    locale_provider = build_locale_provider(cfg.bot.locales_data_path)

    # ugly, but I think it will better in future
    user_repo = UserStorage(session_maker)
    user_service = UserService(
        saver=user_repo,
        getter=user_repo,
        updater=user_repo,
        deleter=user_repo,
        locale_validator=locale_provider
    )

    category_repo = CategoryStorageGateway(session_maker)
    category_rater = FileCategoryUsageRater(session_maker)
    category_service = CategoryService(
        saver=category_repo,
        getter=category_repo,
        finder=category_repo,
        updater=category_repo,
        rater=category_rater,
    )

    file_repo = FileStorageGateway(session_maker)
    file_service = FileService(
        saver=file_repo,
        getter=file_repo,
        finder=file_repo,
        updater=file_repo,
        deleter=file_repo,
        category_getter=category_service
    )

    tg_bot = (
        BotBuilder(cfg=cfg, user_service=user_service, locale_displayer=locale_provider).
        with_fsm_storage(MemoryStorage()).
        build_deps(file_service, category_service).
        build()
    )

    await tg_bot.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("shutdown")
