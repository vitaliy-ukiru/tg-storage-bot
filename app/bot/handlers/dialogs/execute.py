from typing import Optional

from aiogram_dialog import DialogManager, ShowMode, StartMode, Data

from app.bot.states.dialogs import FileViewSG, FileListSG, CategoryEditSG, UserChangeLocaleSG, \
    CategoryCreateSG, UserMenuSG
from app.core.domain.models.category import CategoryId
from app.core.domain.models.file import FileId


async def file_view(manager: DialogManager,
                    file_id: int | FileId,
                    data: Data = None,
                    mode: StartMode = StartMode.RESET_STACK,
                    show_mode: Optional[ShowMode] = None):
    if not isinstance(data, dict):
        data = {}

    await manager.start(
        FileViewSG.main,
        dict(file_id=int(file_id)) | data,
        mode=mode,
        show_mode=show_mode,
    )


async def file_list(manager: DialogManager,
                    filters: dict = None,
                    data: Data = None,
                    mode: StartMode = StartMode.RESET_STACK,
                    show_mode: Optional[ShowMode] = None):
    if filters is not None:
        if data is None:
            data = {}

        data |= filters

    await manager.start(
        FileListSG.main,
        data,
        mode=mode,
        show_mode=show_mode,
    )


async def category_create(manager: DialogManager,
                          data: Data = None,
                          mode: StartMode = StartMode.RESET_STACK,
                          show_mode: Optional[ShowMode] = None):
    await manager.start(
        CategoryCreateSG.input_title,
        data=data,
        mode=mode,
        show_mode=show_mode
    )


async def category_edit(manager: DialogManager,
                        category_id: int | CategoryId,
                        data: Data = None,
                        mode: StartMode = StartMode.NORMAL,
                        show_mode: Optional[ShowMode] = None):
    data = data or {}
    await manager.start(
        CategoryEditSG.main,
        dict(category_id=category_id) | data,
        mode=mode,
        show_mode=show_mode,
    )


async def change_locale(manager: DialogManager,
                        data: Data = None,
                        mode: StartMode = StartMode.RESET_STACK,
                        show_mode: Optional[ShowMode] = None):
    await manager.start(
        UserChangeLocaleSG.main,
        data=data,
        mode=mode,
        show_mode=show_mode,
    )


async def user_menu(manager: DialogManager,
                    data: Data = None,
                    mode: StartMode = StartMode.RESET_STACK,
                    show_mode: Optional[ShowMode] = None):
    await manager.start(
        UserMenuSG.main,
        data=data,
        mode=mode,
        show_mode=show_mode,
    )
