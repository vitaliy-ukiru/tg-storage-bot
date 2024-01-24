from dataclasses import dataclass, field
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.strategy import FSMStrategy
from aiogram_dialog import setup_dialogs

from app.bot.handlers import users, dialogs
from app.bot.middlewares import UserMiddleware
from app.bot.utils.uploader import FileUploader
from app.common.config import Config
from app.core.interfaces.usecase import UserUsecase, CategoryUsecase, FileUsecase


def _configure_dp(dp: Dispatcher, user_service: UserUsecase):
    dp.update.middleware(UserMiddleware(user_service))

    users.setup(dp)
    dialogs.setup(dp)

    setup_dialogs(dp)


@dataclass
class BotModule:
    bot: Bot
    dp: Dispatcher

    async def run(self, **kwargs):
        return await self.dp.start_polling(self.bot, **kwargs)

@dataclass
class BotBuilder:
    cfg: Config
    user_service: UserUsecase
    deps: dict[str, Any] = field(init=False, default_factory=dict)
    dp_name: str | None = None
    fsm_storage: BaseStorage | None = None
    fsm_strategy: FSMStrategy | None = None
    event_isolation: BaseEventIsolation | None = None



    def with_fsm_storage(self, storage: BaseStorage):
        self.fsm_storage = storage
        return self

    def with_event_isolation(self, isolation: BaseEventIsolation | None):
        self.event_isolation = isolation
        return self

    def with_fsm_strategy(self, strategy: FSMStrategy):
        self.fsm_strategy = strategy
        return self

    def with_deps(self, **deps):
        self.deps.update(deps)
        return self

    def build_deps(
        self,
        file_service: FileUsecase,
        category_service: CategoryUsecase,
    ):
        self.deps.update(
            file_service=file_service,
            category_service=category_service,
            user_service=self.user_service,
            uploader=FileUploader(file_service),
            cfg=self.cfg,
        )
        return self

    def with_name(self, name: str):
        self.dp_name = name
        return self

    def _build_bot(self):
        return Bot(
            token=self.cfg.bot.token.get_secret_value(),
            parse_mode=ParseMode.HTML,
        )

    def _build_dp(self) -> Dispatcher:
        dp = Dispatcher(
            storage=self.fsm_storage,
            fsm_strategy=self.fsm_strategy or FSMStrategy.USER_IN_CHAT,
            events_isolation=self.event_isolation,
            disable_fsm=False,
            name=self.dp_name,
            **self.deps
        )
        _configure_dp(dp, self.user_service)
        return dp

    def build(self) -> BotModule:
        return BotModule(
            self._build_bot(),
            self._build_dp(),
        )
