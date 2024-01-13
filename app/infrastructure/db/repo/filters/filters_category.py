from app.core.domain.models.user import UserId
from .container import Container
from ...models import Category

categories = Container()

@categories("user_id")
def _user(value: UserId | int):
    return Category.user_id == value


@categories("title_match")
def _title(title: str):
    return Category.title.icontains(title)


@categories("favorites")
def _favorites(val: bool):
    return Category.is_favorite == val
