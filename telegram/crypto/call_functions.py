import json

from typing import Any, List
from aiogram import Bot
from psycopg2 import connect
from aioredis import Redis
from solana.rpc.async_api import AsyncClient

from .info_functions import Info
from .tx_functions import Transactions
from llm.types import LLM_Message


class Executor(Info, Transactions):
    def __init__(
            self,
            rpc_url: str,
            bot_client: Bot,
            pg_conn: connect,
            redis_conn: Redis
    ):
        self.rpc_client = AsyncClient(rpc_url)
        self.bot_client = bot_client
        self.pg_conn = pg_conn
        self.redis_conn = redis_conn

    async def function_call(self, call_data: dict, messages: List[LLM_Message]) -> [str, Any]:
        """
        Call function by name
        :param messages:
        :param call_data:
        :return: type of function, result
        """

        if 'name' in call_data:
            func = self.__getattribute__(call_data['name'])

            if 'arguments' in call_data:
                kwargs = json.loads(call_data['arguments'])
                return await func(**kwargs, messages=messages)

            return await func()

        return Exception('Wrong call data!')
