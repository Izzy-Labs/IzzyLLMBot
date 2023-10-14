from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_transaction(task_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Reject', callback_data=f'tx-reject/{task_id}')
    button2 = InlineKeyboardButton(text='Confirm', callback_data=f'tx-confirm/{task_id}')
    keyboard.add(button1, button2)
    return keyboard
