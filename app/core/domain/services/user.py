from app.core.interfaces.repository.user import UserRepository
from app.core.interfaces.usecase.user import UserUsecase
from app.core.domain.exceptions.user import UserNotFound, UserDeleted
from app.core.domain.models.user import User, UserId


class UserService(UserUsecase):
    _repo: UserRepository

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def create_user(self, user_id: UserId) -> User:
        return await self._repo.save_user(user_id)

    async def get_user(self, user_id: UserId, force_find: bool = False) -> User:
        user = await self._repo.get_user(user_id)
        if user is None:
            if not force_find:
                raise UserNotFound(user_id)

            user = await self._repo.save_user(user_id)
            return user

        if user.is_deleted:
            if not force_find:
                raise UserDeleted(user_id)

            user = await self._repo.restore_user(user_id)

        return user
