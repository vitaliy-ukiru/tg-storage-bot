from typing import Optional

from aiogram_dialog import DialogManager, ShowMode, StartMode, Data

from bot.handlers.dialogs.file import ViewSG
from core.domain.models.file import FileId


async def file_view(manager: DialogManager, file_id: int | FileId,
                    data: Data = None,
                    mode: StartMode = StartMode.NORMAL,
                    show_mode: Optional[ShowMode] = None):
    data = data or {}
    await manager.start(ViewSG.main, dict(file_id=int(file_id)) | data, mode=mode, show_mode=show_mode)
