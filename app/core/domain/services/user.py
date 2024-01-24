from typing import cast

from app.core.common.locales import ensure_locale
from app.core.domain.dto.user import CreateUserDTO, UpdateLocaleDTO
from app.core.interfaces.repository.user import UserRepository
from app.core.interfaces.usecase.user import UserUsecase
from app.core.domain.exceptions.user import UserNotFound, UserDeleted
from app.core.domain.models.user import User, UserId


class UserService(UserUsecase):
    _repo: UserRepository

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def create_user(self, dto: CreateUserDTO) -> User:
        locale = ensure_locale(dto.locale)
        return await self._repo.save_user(UserId(dto.user_id), locale)

    async def get_user(self, user_id: UserId, restore: bool = False) -> User:
        user = await self._repo.get_user(user_id)
        if user is None:
            raise UserNotFound(user_id)

        if user.is_deleted:
            if not restore:
                raise UserDeleted(user_id)

            user = await self._repo.restore_user(user_id)

        return cast(User, user)

    async def update_locale(self, dto: UpdateLocaleDTO) -> User:
        user = await self._repo.get_user(UserId(dto.user_id))
        user.locale = ensure_locale(dto.locale)
        await self._repo.update_locale(user)
        return user
