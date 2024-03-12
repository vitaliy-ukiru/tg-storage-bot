from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Start

from app.bot.states.dialogs import FileListSG, CategoryCreateSG, UserMenuSG, UploadFileSG
from ._common import TL
from ._open_category import open_category_window
from ._open_file import open_file_window

TL_MAIN = TL.main


async def _on_process_result(_, __, manager: DialogManager):
    await manager.switch_to(UserMenuSG.main)


user_menu_dialog = Dialog(
    Window(
        TL_MAIN.menu.text(),
        Group(
            Start(
                TL_MAIN.upload.file(),
                id="upload_file",
                state=UploadFileSG.main,
            ),
            SwitchTo(
                TL_MAIN.open.file(),
                id="open_file",
                state=UserMenuSG.open_file
            ),
            Start(
                TL_MAIN.find.files(),
                id="find_files",
                state=FileListSG.main,
            ),
            width=2,
        ),
        Group(
            Start(
                TL_MAIN.category.create(),
                id="create_category",
                state=CategoryCreateSG.input_title,
            ),
            SwitchTo(
                TL_MAIN.category.open(),
                id="open_category",
                state=UserMenuSG.open_category
            ),
            width=2
        ),
        state=UserMenuSG.main
    ),

    open_file_window,
    open_category_window,
    on_process_result=_on_process_result
)
