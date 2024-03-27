import secrets

from app.core.domain.dto.token import CreateTokenDTO, TokenDTO, TokenCredentialsDTO
from app.core.domain.exceptions.base import AccessDenied
from app.core.domain.exceptions.token import InvalidToken
from app.core.domain.exceptions.user import UserDeleted
from app.core.domain.models.auth import Operation, Issuer
from app.core.domain.models.token import Token, Scope, TokenInfo
from app.core.domain.models.user import UserId
from app.core.domain.services.access import AccessService
from app.core.interfaces.repository.token import (
    TokenRepoSaver, TokenRepoGetter, TokenRepoDeleter
)
from app.core.interfaces.usecase.token import TokenUsecase
from app.core.interfaces.usecase.user import UserGetter


class TokenService(TokenUsecase):
    def __init__(
        self,
        saver: TokenRepoSaver,
        getter: TokenRepoGetter,
        deleter: TokenRepoDeleter,
        user_getter: UserGetter,
        access: AccessService,
    ):
        self.access = access
        self._saver = saver
        self._getter = getter
        self._deleter = deleter
        self._user_getter = user_getter

    async def save_token(self, token: CreateTokenDTO, issuer: Issuer) -> Token:
        self.access.ensure_have_access(issuer, Operation.token_create)
        user_id = issuer.user_id
        token_id = _new_token_id()

        await self._saver.save_token(
            TokenDTO(
                id=token_id,
                user_id=user_id,
                name=token.name,
                expiry=token.expiry,
                scopes=_scopes_to_list(token.scopes)
            )
        )
        return Token(
            id=token_id,
            user_id=user_id,
        )

    async def get_token(self, token: str) -> TokenInfo:
        creds = _split_token(token)
        token_dto = await self._getter.get_token(creds)
        if not token_dto:
            raise InvalidToken()

        token_info = TokenInfo(
            id=token_dto.id,
            user_id=UserId(token_dto.user_id),
            name=token_dto.name,
            scopes=_scopes_from_list(token_dto.scopes),
            expiry=token_dto.expiry,
        )

        await self._validate_token(token_info)

        return token_info

    async def delete_token(self, token: str, issuer: Issuer):
        self.access.ensure_have_access(issuer, Operation.token_delete)
        creds = _split_token(token)
        if creds.user_id != issuer.user_id:
            raise AccessDenied()

        token = await self._getter.get_token(creds)
        if not token:
            raise InvalidToken()

        await self._deleter.delete_token(creds)

    async def _validate_token(self, token: TokenInfo):
        if token.expired:
            raise InvalidToken()

        try:
            await self._user_getter.get_user(UserId(token.user_id))
        except UserDeleted:
            raise InvalidToken()


def _split_token(token: str) -> TokenCredentialsDTO:
    if any(s.isspace() for s in token):
        raise InvalidToken("Token contains whitespaces")

    user_id, token_id, *other = token.split(':')
    if other:
        raise InvalidToken()
    try:
        user_id = int(user_id)
    except ValueError:
        raise InvalidToken()

    return TokenCredentialsDTO(
        id=token_id,
        user_id=user_id,
    )


TOKEN_LENGTH = 24


def _new_token_id():
    return secrets.token_urlsafe(TOKEN_LENGTH)


def _scopes_to_list(scopes: set[Scope]) -> list[str]:
    return [
        scope.value()

        for scope in scopes
    ]


def _scopes_from_list(scopes: list[str]) -> set[Scope]:
    return {
        Scope(scope)
        for scope in scopes
    }
