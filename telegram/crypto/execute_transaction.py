import json


class Transactions:

    async def exec(self, transaction_name: str, *args, **kwargs) -> str:
        func = self.__getattribute__(transaction_name)

        return await func(*args, **kwargs)

    async def swap(self, *args, **kwargs) -> str:
        resp = json.dumps({
            'result': 'success',
            'tx_id': 'cVf2EoqGw6Fda8Ztjeazx1GAKHu1NQJVtJ1J28Ek8F2BJESHDdMG1WbzvjJfuzKG2ifrXmGR4uzNc1855kdGJKY '
        })

        return resp

    async def swap_to(self, *args, **kwargs) -> str:
        pass

    async def transfer(self, *args, **kwargs) -> str:
        pass

    async def withdraw(self, *args, **kwargs) -> str:
        pass

    async def withdraw_all(self, *args, **kwargs) -> str:
        pass
