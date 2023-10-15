import json

from aiogram import types
from aioredis import Redis
from langchain.schema import HumanMessage, AIMessage, FunctionMessage

from bot.dispatcher import bot
from llm import LLM, function_descriptions, json_to_chat
from crypto.execute_transaction import Transactions


async def tx_reject(query: types.CallbackQuery) -> None:
    """
    Reject transaction
    :param query:
    :return:
    """

    task_id = query.data.split('/')[1]
    chat_id = query.message.chat.id
    redis: Redis = query.redis

    byte_data = await redis.hget('tasks', task_id)
    await redis.hdel('tasks', task_id)

    if not byte_data:
        await bot.send_message(chat_id, 'Transaction already rejected or executed!')
        return

    data = json.loads(byte_data)
    messages = json_to_chat(data['messages'])

    second_response = LLM.predict_messages(
        messages=[
            *messages,
            HumanMessage(content=f'Reject')
        ],
        functions=function_descriptions
    )
    await bot.send_message(chat_id, second_response.content)


async def tx_confirm(query: types.CallbackQuery) -> None:
    """
    Confirm transaction
    :param query:
    :return:
    """

    task_id = query.data.split('/')[1]
    chat_id = query.message.chat.id
    redis: Redis = query.redis

    byte_data = await redis.hget('tasks', task_id)
    await redis.hdel('tasks', task_id)

    if not byte_data:
        await bot.send_message(
            chat_id,
            'Transaction already rejected or executed!'
        )
        return

    data = json.loads(byte_data)

    func = data.get('function')
    params = data.get('params')
    messages = json_to_chat(data.get('messages'))

    try:
        t = Transactions()
        res = await t.exec(func, **params)
    except Exception as error:
        res = f'Error: {error}'

    fix_message = "If the transaction is successful, report it and format the transaction ID as follows: '[tx_id](https://solanabeach.io/transaction/{tx_id})'"

    second_response = LLM.predict_messages(
        messages=[
            *messages,
            FunctionMessage(
                name=func,
                content=res
            ),
            HumanMessage(content=fix_message)
        ],
        functions=function_descriptions
    )

    await bot.send_message(chat_id, second_response.content, parse_mode='Markdown')
