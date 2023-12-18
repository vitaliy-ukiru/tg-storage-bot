from aiogram import Router
from .files import router as files_router
from .categories import router as category_router


def setup(r: Router):
    r.include_routers(files_router, category_router)
