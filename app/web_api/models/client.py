from dataclasses import dataclass
from datetime import datetime

from app.core.domain.models.user import UserId, User
from .auth import Scope


@dataclass
class Token:
    token: str
    user_id: UserId
    name: str
    scopes: set[Scope]
    expired_at: datetime | None

