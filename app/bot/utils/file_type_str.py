from app.core.domain.models.file import FileType

TYPE_PHOTO = "Фото"
TYPE_VIDEO = "Видео"
TYPE_DOCUMENT = "Документ"
TYPE_AUDIO = "Аудио"
TYPE_GIF = "Гиф"
TYPE_UNKNOWN = "Неизвестно"

_FILE_TYPES = {
    FileType.photo: TYPE_PHOTO,
    FileType.video: TYPE_VIDEO,
    FileType.document: TYPE_DOCUMENT,
    FileType.audio: TYPE_AUDIO,
    FileType.gif: TYPE_GIF,
    FileType.unknown: TYPE_UNKNOWN,
}

VALID_TYPES = (
    FileType.photo,
    FileType.video,
    FileType.document,
    FileType.audio,
    FileType.gif,
)

ALL_TYPES = VALID_TYPES + (FileType.unknown,)

_NAMES = tuple(
    (_FILE_TYPES[file_type], file_type)
    for file_type in ALL_TYPES
)

def file_types_with_names() -> tuple[tuple[str, FileType]]:
    return _NAMES

def get_file_type_name(ft: FileType) -> str:
    return _FILE_TYPES[ft]