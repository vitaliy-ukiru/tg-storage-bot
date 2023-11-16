import abc
import enum

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.ui import TelegramComponent
from bot.ui import common
from bot.ui.telegram_component import TelegramMarkup
from core.domain.file import File


class FileView(TelegramComponent, abc.ABC):
    file: File

    def __init__(self, file: File):
        self.file = file

    async def send(self, bot: Bot, chat_id: int):
        text = self._render_text()
        markup = self._build_markup()

        return await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    def _render_text(self) -> str:
        upload_date = self.file.created_at.strftime("%Y-%m-%d %H:%M:%S %Z")
        return '\n'.join((
            f"Название: {self.file.name}",
            f"Категория: {self.file.category_name}",
            f"Тип: {self.file.type.name}",
            f"Дата загрузки: {upload_date}"
        ))

    def _build_markup(self) -> InlineKeyboardMarkup:
        markup = (
            ("Отправить файл", FileViewAction.send),
            ("Изменить файл", FileViewAction.edit),
            ("Удалить файл", FileViewAction.delete),
        )

        return common.create_markup(markup, FileViewFactory, "action", file_id=self.file.id)


class FileViewAction(enum.StrEnum):
    send = enum.auto()
    edit = enum.auto()
    delete = enum.auto()


class FileViewFactory(CallbackData, prefix="file_view"):
    action: FileViewAction
    file_id: int


class FileUploadMarkup(TelegramMarkup, abc.ABC):
    def __init__(self, file_id: int):
        self.file_id = file_id

    def build(self) -> InlineKeyboardMarkup:
        markup = (
            ("upload.ee", "upload.ee"),
            ("telegraph", "telegraph")
        )
        return common.create_markup(markup, FileUploadData, "service", file_id=self.file_id)


class FileUploadData(CallbackData, prefix="file_upload"):
    service: str
    file_id: int


class FileButton:
    def __init__(self, file: File):
        self._file = file

    def build(self) -> InlineKeyboardButton:
        data = FileUploadData(file_id=self._file.id)
        file_name = title if (title := self._file.title) is not None else f'#{self._file.id}'

        return InlineKeyboardButton(text=file_name, callback_data=data.pack())


class FileButtonData(CallbackData, prefix="file_view"):
    file_id: int
