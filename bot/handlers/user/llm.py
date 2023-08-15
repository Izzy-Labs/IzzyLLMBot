from aiogram import types
from langchain.schema import HumanMessage

from llm import LLM, function_descriptions
from bot.dispatcher import bot


async def text_handler(message: types.Message) -> None:
    print(message.text, '\n')
    first_response = LLM.predict_messages(
        messages=[HumanMessage(content=message.text)],
        functions=function_descriptions
    )

    if first_response.additional_kwargs.get('function_call'):
        print(first_response)
    else:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)

