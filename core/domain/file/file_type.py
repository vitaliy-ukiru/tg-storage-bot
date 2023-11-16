__all__ = ('FileType',)

from enum import StrEnum, auto


class FileType(StrEnum):
    unknown = auto()
    text = auto()
    photo = auto()
    video = auto()
    document = auto()
    audio = auto()
    gif = auto()
