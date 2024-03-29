from aiogram.fsm.state import StatesGroup, State


class FileViewSG(StatesGroup):
    main = State()


class FileEditSG(StatesGroup):
    main = State()
    edit_title = State()
    reload_file = State()


class CategoryFindSG(StatesGroup):
    main = State()
    input_title = State()
    select = State()



class CategoryCreateSG(StatesGroup):
    input_title = State()
    menu_idle = State()
    input_desc = State()
    input_marker = State()


class CategoryEditSG(StatesGroup):
    main = State()
    title = State()
    desc = State()
    marker = State()


class FileListSG(StatesGroup):
    main = State()
    input_file_type = State()
    input_file_title = State()
    file_list = State()


ALLOWED_STATES = frozenset({
    FileViewSG.main,
    FileListSG.main,
    FileListSG.file_list,
    CategoryEditSG.main,
})


class UserChangeLocaleSG(StatesGroup):
    main = State()


class UserMenuSG(StatesGroup):
    main = State()
    open_file = State()
    open_category = State()


class UploadFileSG(StatesGroup):
    main = State()
    already_exists = State()
