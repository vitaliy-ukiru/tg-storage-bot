__all__ = ('FileType',)

from enum import Enum, auto


class FileType(Enum):
    unknown = auto()
    text = auto()
    photo = auto()
    document = auto()
    audio = auto()
    gif = auto()
