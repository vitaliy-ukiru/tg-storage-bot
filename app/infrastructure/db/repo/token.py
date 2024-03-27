from sqlalchemy import delete

from app.core.domain.dto.token import TokenDTO, TokenCredentialsDTO
from app.core.interfaces.repository.token import TokenRepoSaver, TokenRepoGetter, TokenRepoDeleter
from app.infrastructure.db import models
from ._base import BaseRepository


class TokenStorageGateway(
    TokenRepoSaver,
    TokenRepoGetter,
    TokenRepoDeleter,

    BaseRepository
):

    async def save_token(self, token: TokenDTO):
        async with self._pool() as session:
            model = models.Token.from_dto(token)
            session.add(model)
            await session.commit()

    async def get_token(self, token: TokenCredentialsDTO) -> TokenDTO | None:
        async with self._pool() as session:
            token: models.Token | None = await session.get(
                models.Token, (token.id, token.user_id)
            )
            if not token:
                return None

            return token.to_dto()

    async def delete_token(self, token: TokenCredentialsDTO):
        async with self._pool() as session:
            sql = delete(models.Token).where(
                models.Token.id == token.id,
                models.Token.user_id == token.id
            )
            await session.execute(sql)
            await session.commit()
