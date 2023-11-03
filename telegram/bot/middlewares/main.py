from aiogram import Dispatcher

from .database import DatabaseMiddleware
from .redis import RedisMiddleware
from .pre_message import PreMessageMiddleware


def register_all_middlewares(dp: Dispatcher) -> None:
    middlewares = (
        DatabaseMiddleware(),
        RedisMiddleware(),
        PreMessageMiddleware()
    )
    for middleware in middlewares:
        dp.middleware.setup(middleware)
