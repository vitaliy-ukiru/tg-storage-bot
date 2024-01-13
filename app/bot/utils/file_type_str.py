from app.core.domain.models.file import FileCategory, SubFileCategory, FileType

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


SUB_CATEGORY_DOC_TEXT = "текст"
SUB_CATEGORY_DOC_IMAGE = "изображение"
SUB_CATEGORY_DOC_VIDEO = "video"
SUB_CATEGORY_DOC_AUDIO = "аудио"

_SUB_CATEGORIES = {
    SubFileCategory.doc_text: SUB_CATEGORY_DOC_TEXT,
    SubFileCategory.doc_image: SUB_CATEGORY_DOC_IMAGE,
    SubFileCategory.doc_video: SUB_CATEGORY_DOC_VIDEO,
    SubFileCategory.doc_audio: SUB_CATEGORY_DOC_AUDIO,
}

def get_sub_category_name(sub_type: SubFileCategory) -> str:
    return _SUB_CATEGORIES[sub_type]

def get_file_category_name(category: FileCategory) -> str:
    return _FILE_CATEGORIES[category]

def get_file_type_full_name(ft: FileType) -> str:
    category = get_file_category_name(ft.category)
    if ft.sub is None:
        return category

    sub_category = get_sub_category_name(ft.sub)
    return f'{category} ({sub_category})'
