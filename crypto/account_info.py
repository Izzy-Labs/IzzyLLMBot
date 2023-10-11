from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey


class AccountInfo:
    client: AsyncClient

    async def get_account_info(self, address: str) -> str:
        pubkey = Pubkey.from_string(address)
        response = await self.client.get_account_info(pubkey)
        return response.value

    async def get_balance(self, address: str) -> int:
        pubkey = Pubkey.from_string(address)
        response = await self.client.get_balance(pubkey)
        return round(response.value / 10 ** 9, 9)
