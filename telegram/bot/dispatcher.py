from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from bot.misc.env import TgKey


bot = Bot(token=TgKey.TOKEN)
dp = Dispatcher(bot)
