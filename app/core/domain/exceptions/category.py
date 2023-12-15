from app.core.domain.exceptions.base import DomainException
from app.core.domain.models.category import CategoryId
from app.core.domain.models.user import UserId


class CategoryException(DomainException):
    domain_name = "category"
    category_id: CategoryId

    def __init__(self, category_id: CategoryId, message: str) -> None:
        self.category_id = category_id
        super().__init__(message)

    def _get_message(self):
        message = super()._get_message()
        return f'{message} category_id={self.category_id}'


class StaticCategoryException(CategoryException):
    MESSAGE = ""

    def __init__(self, category_id: CategoryId) -> None:
        super(StaticCategoryException, self).__init__(category_id, self.MESSAGE)


class CategoryNotFound(StaticCategoryException):
    MESSAGE = "category not found"


class CategoryViolation(CategoryException):
    user: UserId

    def __init__(self, category_id: CategoryId, user: UserId) -> None:
        self.user = user
        super().__init__(category_id, f"user don't own category {user!r}")
