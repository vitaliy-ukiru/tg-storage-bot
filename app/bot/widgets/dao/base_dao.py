from aiogram_dialog import DialogManager

from app.bot.widgets.dao import ManagerFieldProvider


class BaseDAO(ManagerFieldProvider):
    _manager: DialogManager

    def __init__(self, manager: DialogManager):
        self._manager = manager

    @property
    def manager(self) -> DialogManager:
        return self._manager
