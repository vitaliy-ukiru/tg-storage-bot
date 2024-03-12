from abc import abstractmethod
from typing import Protocol

from app.web_api.models.client import Token


class TokenUsecase(Protocol):
    @abstractmethod
    async def get_token(self, token: str) -> Token:
        raise NotImplementedError

