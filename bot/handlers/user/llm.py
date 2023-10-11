from aiogram import types
from langchain.schema import HumanMessage, AIMessage, SystemMessage, FunctionMessage

from llm import LLM, function_descriptions
from bot.dispatcher import bot
from crypto import Executor


crypto = Executor("https://api.mainnet-beta.solana.com")


async def text_handler(message: types.Message) -> None:
    print(message.text, '\n')
    first_response = LLM.predict_messages(
        messages=[
            HumanMessage(content=message.text)
        ],
        functions=function_descriptions
    )

    if first_response.additional_kwargs.get('function_call'):
        function_result = await crypto.function_call(
            first_response.additional_kwargs['function_call'],
        )
        function_name = first_response.additional_kwargs['function_call']['name']
        print(function_result, '\n')

        second_response = LLM.predict_messages(
            messages=[
                HumanMessage(content=message.text),
                AIMessage(content=str(first_response.additional_kwargs)),
                FunctionMessage(
                    name=function_name,
                    content=str(function_result)
                )
            ],
            functions=function_descriptions
        )
        print(second_response)
        await bot.send_message(chat_id=message.from_user.id, text=second_response.content)

    else:
        await bot.send_message(chat_id=message.from_user.id, text=message.text)

