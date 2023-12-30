from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineQuery,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedGif,
)

from app.core.common.filters.file import FileFilters
from app.core.domain.exceptions.file import FileException, FileNotFound
from app.core.domain.models.file import File, FileType, FileId
from app.core.domain.models.user import User
from app.core.interfaces.usecase import FileUsecase

router = Router()

_FILES_NOT_FOUND = "__files_not_found"


@router.message(CommandStart(deep_link=True, magic=F.args == _FILES_NOT_FOUND))
async def _files_not_found(m: Message):
    await m.answer("По такому запросу файлов не найдено")


@router.inline_query(F.query.cast(int))
async def _find_file_by_id(inline_query: InlineQuery, file_service: FileUsecase, user: User):
    file_id = FileId(int(inline_query.query))
    try:
        file = await file_service.get_file(
            file_id,
            user.id,
        )
        # seen something bad
        if file.type == FileType.unknown:
            raise FileNotFound(file_id)

    except FileNotFound:
        await inline_query.answer(
            [],
            is_personal=True,
            switch_pm_text="Ничего не найдено",
            switch_pm_parameter=_FILES_NOT_FOUND
        )
        return

    await inline_query.answer(
        results=[_convert_to_result(file)]
    )


@router.inline_query()
async def _find_files_by_title(inline_query: InlineQuery, file_service: FileUsecase, user: User):
    files, _ = await file_service.find_files(
        FileFilters.user_id(user.id),
        FileFilters.title_match(inline_query.query)
    )

    if len(files) == 0:
        await inline_query.answer(
            [],
            is_personal=True,
            switch_pm_text="Ничего не найдено",
            switch_pm_parameter=_FILES_NOT_FOUND
        )
        return

    results = [
        _convert_to_result(file)
        for file in files
        if file.type != FileType.unknown
    ]

    await inline_query.answer(
        results=results,
        # cache_time=10*60*60,  # 10 minutes
        is_personal=True,
    )


# don't add return type, because it will be a big typing.Union
# if add like InlineQueryResult type checker will say
# what InlineQuery.answer accepts Union[...]
def _convert_to_result(file: File):
    __result_types = {
        FileType.photo: InlineQueryResultCachedPhoto,
        FileType.video: InlineQueryResultCachedVideo,
        FileType.document: InlineQueryResultCachedDocument,
        FileType.audio: InlineQueryResultCachedAudio,
        FileType.gif: InlineQueryResultCachedGif,
    }

    params = dict(id=f'{file.type}_{file.id}', title=file.title, caption=file.title)

    inline_result_type = __result_types.get(file.type)
    if inline_result_type is None:
        raise FileException(file.id, "file type is not supported for inline query")

    if file.type == FileType.audio:
        del params["title"]

    params[f'{file.type}_file_id'] = file.remote_file_id
    return inline_result_type(**params)
