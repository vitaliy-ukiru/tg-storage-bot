from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Group
from aiogram_dialog.widgets.text import Const

from app.bot.states.dialogs import FileListSG, CategoryCreateSG


class UserMenuSG(StatesGroup):
    main = State()
    upload_file = State()
    open_file = State()
    open_category = State()


user_menu = Dialog(
    Window(
        Group(
            SwitchTo(
                Const("Загрузить файл"),
                id="upload_file",
                state=UserMenuSG.upload_file,
            ),
            SwitchTo(
                Const("Поиск файлов"),
                id="find_file",
                state=FileListSG.main,
            ),
            SwitchTo(
                Const("Открыть файл"),
                id="open_file",
                state=UserMenuSG.open_file
            ),
            width=2,
        ),
        SwitchTo(
            Const("Создать категорию"),
            id="create_category",
            state=CategoryCreateSG.input_title,
        ),
        state=UserMenuSG.main
    ),
    # Window(
    #     MessageInput(_on_send_file, filter=MediaFilter()),
    #     state=UserMenuSG.upload_file
    # )
)
