import mimetypes
from typing import Optional

from app.core.domain.models.file import FileCategory, FileType

CATEGORY_PHOTO = "Фото"
CATEGORY_VIDEO = "Видео"
CATEGORY_DOCUMENT = "Документ"
CATEGORY_AUDIO = "Аудио"
CATEGORY_GIF = "Гиф"
CATEGORY_UNKNOWN = "Неизвестно"

_FILE_CATEGORIES = {
    FileCategory.photo: CATEGORY_PHOTO,
    FileCategory.video: CATEGORY_VIDEO,
    FileCategory.document: CATEGORY_DOCUMENT,
    FileCategory.audio: CATEGORY_AUDIO,
    FileCategory.gif: CATEGORY_GIF,
    FileCategory.unknown: CATEGORY_UNKNOWN,
}

VALID_CATEGORIES = (
    FileCategory.photo,
    FileCategory.video,
    FileCategory.document,
    FileCategory.audio,
    FileCategory.gif,
)

ALL_TYPES = VALID_CATEGORIES + (FileCategory.unknown,)

_CATEGORIES_NAMES = tuple(
    (_FILE_CATEGORIES[file_type], file_type)
    for file_type in ALL_TYPES
)


def file_categories_with_names() -> tuple[tuple[str, FileCategory]]:
    return _CATEGORIES_NAMES


SUB_CATEGORY_TEXT = "текст"
SUB_CATEGORY_IMAGE = "изображение"
SUB_CATEGORY_VIDEO = "видео"
SUB_CATEGORY_AUDIO = "аудио"


def format_mime_type(mime: Optional[str]) -> Optional[str]:
    if mime is None:
        return None

    not_common = all(
        not mime.startswith(type_)
        for type_ in ('text/plaint', "application/octet-stream")
    )

    if not_common:
        ext = mimetypes.guess_extension(mime, strict=False)
        if ext is not None:
            if ext.startswith('.'):
                ext = ext[1:]

            return ext.upper()

    base, *_ = mime.split('/', 2)
    match base:
        case "image":
            return SUB_CATEGORY_IMAGE
        case "video":
            return SUB_CATEGORY_VIDEO
        case "audio":
            return SUB_CATEGORY_AUDIO
        case "text":
            return SUB_CATEGORY_TEXT
        case _:
            return None


def get_file_category_name(category: FileCategory) -> str:
    return _FILE_CATEGORIES[category]

def get_file_type_full_name(ft: FileType) -> str:
    category = get_file_category_name(ft.category)
    sub = format_mime_type(ft.mime)
    if sub is None:
        return category

    return f'{category} ({sub})'
