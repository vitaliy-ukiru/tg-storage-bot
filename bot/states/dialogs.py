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
    input_title = State()
    find = State()


class CategorySelectSG(StatesGroup):
    start = State()


class CategoryCreateSG(StatesGroup):
    input_title = State()
    menu_idle = State()
    input_desc = State()


class FilterSG(StatesGroup):
    main = State()
    file_type = State()
    file_title = State()


class FileListSG(StatesGroup):
    main = State()
    file_list = State()
