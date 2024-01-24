import mimetypes
from typing import Optional

from aiogram_i18n import I18nContext

from app.core.domain.models.file import FileType, FileCategory

SUB_TYPE_KEY = "file-sub-type"
FILE_TYPE_CATEGORY_KEY = 'file-type-category'

VALID_CATEGORIES = (
    FileCategory.photo,
    FileCategory.video,
    FileCategory.document,
    FileCategory.audio,
    FileCategory.gif,
)

ALL_TYPES = VALID_CATEGORIES + (FileCategory.unknown,)


def get_file_category_name(category: FileCategory, i18n: I18nContext) -> str:
    return i18n.get(FILE_TYPE_CATEGORY_KEY, file_type=category.value)


def file_categories_with_names(i18n: I18nContext) -> tuple[tuple[str, FileCategory]]:
    return tuple(
        (get_file_category_name(ft, i18n), ft)
        for ft in ALL_TYPES
    )


ALLOWED_COMMON_SUB_TYPES = frozenset({"image", "video", "audio", "text", })


def format_mime_type(mime: Optional[str], i18n: I18nContext) -> Optional[str]:
    if mime is None:
        return None

    not_common = all(
        not mime.startswith(type_)
        for type_ in ('text/plain', "application/octet-stream")
    )

    if not_common:
        ext = mimetypes.guess_extension(mime, strict=False)
        if ext is not None:
            if ext.startswith('.'):
                ext = ext[1:]

            return ext.upper()

    base, *_ = mime.split('/', 2)
    if base not in ALLOWED_COMMON_SUB_TYPES:
        return None

    return i18n.get(SUB_TYPE_KEY, sub_type=base)


def locale_file_type(ft: FileType, i18n: I18nContext) -> str:
    category = get_file_category_name(ft.category, i18n)
    sub = format_mime_type(ft.mime, i18n)
    if sub is None:
        return category

    return f'{category} ({sub})'
