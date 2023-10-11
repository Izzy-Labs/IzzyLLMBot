import json

from typing import Any
from solana.rpc.async_api import AsyncClient

from .account_info import AccountInfo


class Executor(AccountInfo):
    def __init__(self, rpc_url: str):
        self.client = AsyncClient(rpc_url)

    async def function_call(self, call_data: dict) -> Any:
        if 'name' in call_data:
            func = self.__getattribute__(call_data['name'])

            if 'arguments' in call_data:
                kwargs = json.loads(call_data['arguments'])
                return await func(**kwargs)

            return await func()

        return Exception('Wrong call data!')
