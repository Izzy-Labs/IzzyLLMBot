from aiogram import types
from langchain.schema import HumanMessage, AIMessage, FunctionMessage

from llm import LLM, function_descriptions
from bot.dispatcher import bot
from bot.misc.utils import get_wallet_by_user_id
from crypto import Executor


async def text_handler(message: types.Message, **kwargs) -> None:
    pg_conn = kwargs['pg_conn']
    redis_conn = kwargs['redis']

    executor = Executor(
        rpc_url="https://api.mainnet-beta.solana.com",
        bot_client=bot,
        pg_conn=pg_conn,
        redis_conn=redis_conn,
    )

    user_wallet = get_wallet_by_user_id(message.from_user.id, pg_conn)

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

    print(first_response)

    if first_response.additional_kwargs.get('function_call'):
        function_name = first_response.additional_kwargs['function_call']['name']

        function_type, function_result = await executor.function_call(
            call_data=first_response.additional_kwargs['function_call'],
            messages=[
                HumanMessage(content=message_with_user_data),
                AIMessage(content=str(first_response.additional_kwargs))
            ]
        )

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
