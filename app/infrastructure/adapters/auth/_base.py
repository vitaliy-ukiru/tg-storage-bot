from abc import abstractmethod

from app.core.domain.exceptions.category import CategoryAccessDenied
from app.core.domain.exceptions.file import FileAccessDenied
from app.core.domain.models.category import Category
from app.core.domain.models.file import File
from app.core.domain.models.user import UserId
from app.core.interfaces.access import AccessController, Operation


class BaseAccessController(AccessController):
    def __init__(self, user_id: UserId):
        self.user_id = user_id

    @abstractmethod
    def ensure_have_access(self, op: Operation):
        raise NotImplementedError

    def ensure_own_category(self, category: Category):
        if category.user_id != self.user_id:
            raise CategoryAccessDenied(category.id, self.user_id)

    def ensure_own_file(self, file: File):
        if file.user_id != self.user_id:
            raise FileAccessDenied(file.id, self.user_id)

    def get_current_user_id(self) -> UserId:
        return self.user_id
