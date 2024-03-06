from aiogram import Router
from .categories import router as category_router
from .errors import router as errors_router
from .files import router as files_router
from .inline import router as inline_router
from .user import router as user_router


def setup(r: Router):
    r.include_routers(user_router)
    r.include_routers(errors_router)
    r.include_routers(files_router, category_router)
    r.include_router(inline_router)
