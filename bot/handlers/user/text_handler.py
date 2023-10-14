from time import time

from aiogram import types
from langchain.schema import HumanMessage, AIMessage, SystemMessage, FunctionMessage

from llm import LLM, function_descriptions
from bot.dispatcher import bot
from bot.misc.utils import get_wallet_by_user_id
from crypto import Executor


async def text_handler(message: types.Message) -> None:
    executor = Executor(
        rpc_url="https://api.mainnet-beta.solana.com",
        bot_client=bot,
        pg_conn=message.pg_conn,
        redis_conn=message.redis,
    )

    user_wallet = get_wallet_by_user_id(message.from_user.id, message.pg_conn)

    message_with_user_data = (f"username: {message.from_user.username}, "
                              f"user id: {message.from_user.id}, "
                              f"user`s wallet address: {user_wallet}, "
                              f"text: {message.text}")

    print(message_with_user_data, '\n')

    first_response = LLM.predict_messages(
        messages=[
            HumanMessage(content=message_with_user_data)
        ],
        functions=function_descriptions
    )

    if first_response.additional_kwargs.get('function_call'):
        function_type, function_result = await executor.function_call(
            first_response.additional_kwargs['function_call'],
        )
        print(function_result, '\n')
        function_name = first_response.additional_kwargs['function_call']['name']

        if function_type == 'info':
            second_response = LLM.predict_messages(
                messages=[
                    HumanMessage(content=message_with_user_data),
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

