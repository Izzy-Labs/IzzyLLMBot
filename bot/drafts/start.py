import os
import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

with open('../../LLM/function_descriptions.json', 'r') as file:
    function_descriptions = json.load(file)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message) -> None:
    await message.reply("Hi, Write me something")


@dp.message_handler(content_types='text')
async def message_handler(message: types.Message) -> None:
    user_request = message.text
    first_response = llm.predict_messages([HumanMessage(content=user_request)],
                                          functions=function_descriptions)
    if first_response.additional_kwargs.get('function_call'):
        print(first_response)
    else:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
