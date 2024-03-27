from dataclasses import dataclass
from datetime import datetime

from app.core.domain.models.token import Scope


@dataclass(frozen=True)
class CreateTokenDTO:
    scopes: set[Scope]
    name: str
    expiry: datetime | None = None


@dataclass(frozen=True)
class TokenCredentialsDTO:
    id: str
    user_id: int


@dataclass(frozen=True)
class TokenDTO:
    id: str
    user_id: int
    scopes: list[str]
    name: str
    expiry: datetime | None = None
