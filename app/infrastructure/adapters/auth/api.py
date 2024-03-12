from typing import Sequence

from app.core.domain.exceptions.base import AccessDenied
from app.web_api.models.auth import Scope
from app.core.domain.models.user import UserId
from app.core.interfaces.access import Operation
from app.infrastructure.adapters.auth._base import BaseAccessController

_OPERATION_TO_SCOPE = {
    Operation.category_create: Scope.category_create,
    Operation.category_edit: Scope.category_edit,
    Operation.file_create: Scope.file_create,
    Operation.file_edit: Scope.file_edit,
    Operation.file_delete: Scope.file_delete,
}


class ApiAccessController(BaseAccessController):
    def __init__(self, scopes: Sequence[Scope], user_id: UserId):
        self.scopes = set(scopes)
        super().__init__(user_id)

    def ensure_have_access(self, op: Operation):
        scope = _OPERATION_TO_SCOPE.get(op, None)
        if not scope:  # decline unknown operation
            raise AccessDenied()

        if scope not in self.scopes:
            raise AccessDenied()
