from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.states import EditFile
from bot.ui.file import FileView, FileViewFactory, FileViewAction, FileEdit
from core.domain.file.service import FileService


router = Router(name="file-view-router")


@router.callback_query(FileViewFactory.filter(F.action == FileViewAction.send))
async def process_send_file(callback: CallbackQuery, service: FileService,
                            callback_data: FileViewFactory):
    file = await service.get_file_by_id(callback_data.file_id)
    view = FileView(file)
    await view.send_media(callback.bot, callback.chat.id)


@router.callback_query(FileViewFactory.filter(F.action == FileViewAction.edit))
async def process_edit_file_menu(call: CallbackQuery, callback_data: FileViewFactory, state: FSMContext):
    await state.set_state(EditFile.menu_idle)
    await state.update_data(file_id=callback_data.file_id)
    msg = FileEdit(callback_data.file_id)
    await call.message.edit_text(text=msg.text, reply_markup=msg.markup)


@router.callback_query(FileViewFactory.filter(F.action == FileViewAction.delete))
async def process_delete_file(callback: CallbackQuery):
    await callback.answer(text="Not implemented at service", show_alert=True)
