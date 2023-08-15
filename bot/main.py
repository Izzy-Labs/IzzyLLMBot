from aiogram.utils import executor
from aiogram import Dispatcher

from bot.dispatcher import dp
from bot.filters import register_all_filters
from bot.handlers import register_all_handlers


async def __on_start_up__(dispatcher: Dispatcher) -> None:
    register_all_filters(dispatcher)
    register_all_handlers(dispatcher)


def start_bot():
    executor.start_polling(
        dispatcher=dp,
        on_startup=__on_start_up__
    )
