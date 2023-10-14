from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class TxRejectFilter(BoundFilter):
    key = 'is_reject_transaction'

    def __init__(self, is_reject_transaction: bool):
        self.is_reject_transaction = is_reject_transaction

    async def check(self, query: types.CallbackQuery):
        return query.data.startswith('tx-reject')


class TxConfirmFilter(BoundFilter):
    key = 'is_confirm_transaction'

    def __init__(self, is_confirm_transaction: bool):
        self.is_confirm_transaction = is_confirm_transaction

    async def check(self, query: types.CallbackQuery):
        return query.data.startswith('tx-confirm')
