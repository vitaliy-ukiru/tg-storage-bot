__all__ = (
    'TokenSaver',
    'TokenGetter',
    'TokenDeleter',
    'TokenUsecase',
)
from abc import abstractmethod
from typing import Protocol

from app.core.domain.dto.token import CreateTokenDTO
from app.core.domain.models.token import Token, TokenInfo
from app.core.domain.models.auth import Issuer


class TokenSaver(Protocol):
    @abstractmethod
    async def save_token(self, token: CreateTokenDTO, issuer: Issuer) -> Token:
        raise NotImplementedError


class TokenGetter(Protocol):
    @abstractmethod
    async def get_token(self, token: str) -> TokenInfo:
        raise NotImplementedError


class TokenDeleter(Protocol):
    @abstractmethod
    async def delete_token(self, token: str, issuer: Issuer):
        raise NotImplementedError

class TokenUsecase(
    TokenSaver,
    TokenDeleter,
    TokenGetter,
):
    pass