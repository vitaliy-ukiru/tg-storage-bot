from aiogram.fsm.state import StatesGroup, State


class FileViewSG(StatesGroup):
    main = State()
    send_file = State()


class FileEditSG(StatesGroup):
    main = State()
    edit_title = State()
    reload_file = State()


class CategoryFindSG(StatesGroup):
    main = State()
    top = State()
    favorites = State()
    input_title = State()
    find = State()


class CategorySelectSG(StatesGroup):
    start = State()


class CategoryCreateSG(StatesGroup):
    input_title = State()
    menu_idle = State()
    input_desc = State()

class CategoryEditSG(StatesGroup):
    main = State()
    title = State()
    desc = State()


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