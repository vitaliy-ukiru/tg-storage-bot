from .container import Container
from .filters_file import files as _files_container
from .filters_category import categories as _categories_container


# noinspection PyMethodParameters
class Registry:
    files = _files_container
    categories = _categories_container
