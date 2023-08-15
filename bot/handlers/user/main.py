from aiogram import Dispatcher

from .basic import start, help
from .llm import text_handler


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help, commands=["help"])

    dp.register_message_handler(text_handler, content_types="text")
