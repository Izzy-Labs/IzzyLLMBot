from aiogram import Dispatcher

from .basic import start, help
from .text_handler import text_handler
from .processing_transactions import tx_reject, tx_confirm


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help, commands=["help"])

    dp.register_message_handler(text_handler, content_types="text")

    dp.register_callback_query_handler(tx_reject, is_reject_transaction=True)
    dp.register_callback_query_handler(tx_confirm, is_confirm_transaction=True)
