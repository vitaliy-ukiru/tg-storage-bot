from app.core.domain.models.user import UserId
from app.core.interfaces.repository.common import FilterField


class CategoryFilters:
    @classmethod
    def user_id(cls, value: UserId | int) -> FilterField[UserId | int]:
        return FilterField("user_id", value)

    @classmethod
    def title_match(cls, value: str) -> FilterField[str]:
        return FilterField("title_match", value)

    @classmethod
    def favorites(cls, favorites: bool = True) -> FilterField[bool]:
        return FilterField("favorites", favorites)
