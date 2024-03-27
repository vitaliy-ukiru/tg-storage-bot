from app.core.domain.exceptions.base import AccessDenied
from app.core.domain.exceptions.category import CategoryAccessDenied
from app.core.domain.exceptions.file import FileAccessDenied
from app.core.domain.models.auth import IssuerType, Issuer, Operation
from app.core.domain.models.category import Category
from app.core.domain.models.file import File

ONLY_TELEGRAM_ALLOWED = frozenset({
    Operation.token_create,
    Operation.token_delete,
})


class AccessService:
    def __init__(self):
        pass

    @staticmethod
    def ensure_have_access(issuer: Issuer, op: Operation):
        if not issuer.can(op):
            raise AccessDenied()

        if op in ONLY_TELEGRAM_ALLOWED and issuer.issuer_type != IssuerType.TELEGRAM:
            raise AccessDenied()

    @staticmethod
    def ensure_own_category(issuer: Issuer, category: Category):
        if category.user_id != issuer.user_id:
            raise CategoryAccessDenied(category.id, issuer.user_id)

    @staticmethod
    def ensure_own_file(issuer: Issuer, file: File):
        if file.user_id != issuer.user_id:
            raise FileAccessDenied(file.id, issuer.user_id)
