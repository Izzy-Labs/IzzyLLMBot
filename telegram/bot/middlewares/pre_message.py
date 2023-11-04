from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.locales import get_text


class PreMessageMiddleware(BaseMiddleware):
    """
    Middleware for adding redis connection to message
    """
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message, data: dict) -> None:
        """
        Add redis connection to message
        :param message:
        :param data:
        :return:
        """

        base_text = get_text('waiting for bot answer')
        sent_message = await message.answer(base_text)

        data['message_id'] = sent_message.message_id
