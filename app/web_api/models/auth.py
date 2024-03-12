from enum import StrEnum, auto


class ScopeEnumType(StrEnum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().replace("_", ":", 1)


class Scope(ScopeEnumType):
    category_create = auto()  # = "category:create"
    category_edit = auto()  # = "category:edit"
    file_create = auto()  # = "file:create"
    file_edit = auto()  # = "file:edit"
    file_delete = auto()  # = "file:delete"


