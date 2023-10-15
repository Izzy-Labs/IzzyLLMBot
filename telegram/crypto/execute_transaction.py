import json


class Transactions:

    async def exec(self, transaction_name: str, *args, **kwargs) -> str:
        func = self.__getattribute__(transaction_name)

        return await func(*args, **kwargs)

    async def swap(self, *args, **kwargs) -> str:
        print(f'swap: {args}, {kwargs}')
        resp = json.dumps({
            'result': 'ok',
            'tx_id': '2PStA6wUbyH5RFNz9aV3aWxL21GgSCnL4BgM32ka8x3QntuQiVr5hjaTd7CsTcNGzJK6wgaPrPPidzwvaNgysQ2V'
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
