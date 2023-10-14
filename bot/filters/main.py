from aiogram import Dispatcher

from .transaction_buttons import TxConfirmFilter, TxRejectFilter


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(TxConfirmFilter)
    dp.filters_factory.bind(TxRejectFilter)
