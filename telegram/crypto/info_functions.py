from typing import Union, List

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from bot.misc.utils import check_wallet_address
from llm.types import Message


class Info:
    rpc_client: AsyncClient

    async def get_account_info(self, address: Union[str, None], messages: List[Message] = None) -> [str, str]:
        """
        Get account info by address
        :param messages:
        :param address: wallet address
        :return: type of function, account info
        """

        try:
            check_wallet_address(address)
        except ValueError as error:
            return str(error)

        pubkey = Pubkey.from_string(address)
        response = await self.rpc_client.get_account_info(pubkey)

        return 'info', response.value

    async def get_balance(self, address: str, messages: List[Message] = None) -> [str, str]:
        """
        Get balance by address
        :param messages:
        :param address: wallet address
        :return: type of function, balance
        """

        try:
            check_wallet_address(address)
        except ValueError as error:
            return str(error)

        pubkey = Pubkey.from_string(address)
        response = await self.rpc_client.get_balance(pubkey)
        result = str(round(response.value / 10 ** 9, 9))

        return 'info', result

    @staticmethod
    async def get_connected_wallet(address: str, messages: List[Message] = None) -> [str, str]:
        """
        Get connected wallet
        :param messages:
        :param address:  address
        :return: type of function, wallet address
        """
        try:
            check_wallet_address(address)
        except ValueError as error:
            return str(error)

        return 'info', address
