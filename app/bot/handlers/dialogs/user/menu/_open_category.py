from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import DialogManager, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Case

from app.bot.states.dialogs import UserMenuSG
from app.bot.widgets.i18n import Template, BackToI18n
from app.core.domain.exceptions.category import CategoryNotFound, CategoryAccessDenied
from app.core.domain.models.category import CategoryId
from app.core.domain.models.user import User
from app.core.interfaces.usecase import CategoryUsecase
from ._common import TL, _number_filter, _error_getter
from app.bot.handlers.dialogs import execute

OPEN_CATEGORY_ERROR_KEY = "open_category_error"


async def _on_input_category(m: Message, _, manager: DialogManager):
    category_id = CategoryId(int(m.text))
    user: User = manager.middleware_data["user"]
    category_service: CategoryUsecase = manager.middleware_data["category_service"]
    try:
        category = await category_service.get_category(category_id, user.id)
    except (CategoryNotFound, CategoryAccessDenied) as exp:
        manager.dialog_data[OPEN_CATEGORY_ERROR_KEY] = exp
        return

    await execute.category_edit(manager, category.id, mode=StartMode.NORMAL)


open_category_window = Window(
    Case(
        {
            CategoryNotFound: Template("category-not-found"),
            CategoryAccessDenied: Template("category-access-denied"),
        },
        selector="error_type",
        when="error_type",
    ),
    TL.category.enter(),
    MessageInput(_on_input_category, ContentType.TEXT, _number_filter),
    BackToI18n(UserMenuSG.main),
    state=UserMenuSG.open_category,
    getter=_error_getter(OPEN_CATEGORY_ERROR_KEY),
)
