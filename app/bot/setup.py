from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import setup_dialogs
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.bot.handlers import users, dialogs
from app.bot.middlewares import UserMiddleware, FileProxyMiddleware, CategoryProxyMiddleware, \
    FileUploaderMiddleware
from app.common.config import TelegramConfig
from app.core.interfaces.usecase import UserUsecase, CategoryUsecase, FileUsecase
from app.infrastructure.adapters.locale_manager import LazyGatewayLocaleManager, GatewayLocaleManager, \
    ContextLocaleManager


def _configure_dp(
    user_service: UserUsecase,
    category_service: CategoryUsecase,
    file_service: FileUsecase,
    storage: Optional[BaseStorage] = None,
) -> Dispatcher:
    dp = Dispatcher(storage=storage)
    dp.update.middleware(UserMiddleware(user_service))
    dp.update.middleware(FileProxyMiddleware(file_service))
    dp.update.middleware(CategoryProxyMiddleware(category_service))
    dp.message.middleware(FileUploaderMiddleware(file_service))
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="app/bot/locales/{locale}"
        ),
        manager=LazyGatewayLocaleManager(
            GatewayLocaleManager(user_service),
            ContextLocaleManager()
        )
    )

    users.setup(dp)
    dialogs.setup(dp)

    # dp.message.register(start, CommandStart())
    i18n_middleware.setup(dp)
    setup_dialogs(dp)
    return dp


class BotModule:
    def __init__(
        self,
        cfg: TelegramConfig,
        user_service: UserUsecase,
        category_service: CategoryUsecase,
        file_service: FileUsecase,
        storage: Optional[BaseStorage] = None,
    ):
        self.bot = Bot(token=cfg.token.get_secret_value(), parse_mode=ParseMode.HTML)
        self.dp = _configure_dp(user_service, category_service, file_service, storage)

    async def run(self):
        return await self.dp.start_polling(self.bot)
