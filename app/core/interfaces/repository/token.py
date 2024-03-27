from abc import abstractmethod
from typing import Protocol

from app.core.domain.dto.token import TokenDTO, TokenCredentialsDTO


class TokenRepoSaver(Protocol):
    @abstractmethod
    async def save_token(self, token: TokenDTO):
        raise NotImplementedError


class TokenRepoGetter(Protocol):
    @abstractmethod
    async def get_token(self, token: TokenCredentialsDTO) -> TokenDTO | None:
        raise NotImplementedError


class TokenRepoDeleter(Protocol):
    @abstractmethod
    async def delete_token(self, token: TokenCredentialsDTO):
        raise NotImplementedError
