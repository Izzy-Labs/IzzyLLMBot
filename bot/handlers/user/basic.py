from aiogram import types
from bot.locales import get_text


async def start(message: types.Message) -> None:
    await message.answer(get_text("start", "us"))


async def help(message: types.Message) -> None:
    await message.answer("Here's a list of available commands:\n/help - Show this help message\n/start - Start the bot")
