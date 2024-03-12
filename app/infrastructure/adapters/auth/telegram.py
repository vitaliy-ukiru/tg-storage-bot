from app.web_api.models.auth import Scope
from ._base import BaseAccessController


class TelegramAccessController(BaseAccessController):
    def ensure_have_access(self, scope: Scope):
        return  # pass all rights

