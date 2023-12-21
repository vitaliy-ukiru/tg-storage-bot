from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import setup_dialogs

from app.bot.handlers import users, dialogs
from app.bot.middlewares import UserMiddleware, FileProxyMiddleware, CategoryProxyMiddleware, \
    FileUploaderMiddleware
from app.common.config import TgBot
from app.core.interfaces.usecase import UserUsecase, CategoryUsecase, FileUsecase


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

    users.setup(dp)
    dialogs.setup(dp)

    # dp.message.register(start, CommandStart())
    setup_dialogs(dp)
    return dp

class BotModule:
    def __init__(
        self,
        cfg: TgBot,
        user_service: UserUsecase,
        category_service: CategoryUsecase,
        file_service: FileUsecase,
        storage: Optional[BaseStorage] = None,
    ):
        self.bot = Bot(token=cfg.token, parse_mode=ParseMode.HTML)
        self.dp = _configure_dp(user_service, category_service, file_service, storage)

    async def run(self):
        return await self.dp.start_polling(self.bot)