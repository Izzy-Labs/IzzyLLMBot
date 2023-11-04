import json
import asyncio
import requests

from aiogram import types
from aioredis import Redis
from psycopg2 import connect
from solders.pubkey import Pubkey

from .exceptions import RedisTaskNotFoundException


DEXSCREENER_LINK = 'https://api.dexscreener.com/latest/dex/search?q='


def get_wallet_by_user_id(user_id: int, pg_conn: connect) -> str:
    if pg_conn:
        cursor = pg_conn.cursor()
        request = "SELECT address FROM users WHERE id = %s"
        cursor.execute(request, (user_id,))
        address = cursor.fetchone()
        cursor.close()
        return address[0] if address else None

    return None


def check_wallet_address(address: str) -> None:
    if any([
        address is None,
        address == '',
        address.lower() == 'none',
        address.lower() == 'null'
    ]):
        raise ValueError('wallet public key not found')

    try:
        Pubkey.from_string(address)
    except ValueError:
        raise ValueError(f'wallet public key is invalid: {address}')


def get_token_address(token_name: str) -> str:
    token_name = token_name.upper()

    response = requests.get(
        DEXSCREENER_LINK + token_name,
    ).json()

    for pair in response['pairs']:
        if pair['chainId'] == 'solana':
            if (pair['baseToken']['symbol'] == token_name or
                    pair['quoteToken']['symbol'] == token_name):
                return pair['baseToken']['address']
            return pair['quoteToken']['address']

    raise ValueError(f'token {token_name} not found')


def get_quote_token_price(
        from_token_name: str,
        to_token_name: str,
) -> float:
    from_token_name = from_token_name.upper()
    to_token_name = to_token_name.upper()

    link = f"{DEXSCREENER_LINK}{from_token_name}%20{to_token_name}"
    response = requests.get(link).json()

    for pair in response['pairs']:
        if pair['chainId'] == 'solana':
            if pair['baseToken']['symbol'] == from_token_name:
                return float(pair['priceNative'])
            elif pair['quoteToken']['symbol'] == from_token_name:
                return 1 / float(pair['priceNative'])

    return None


def get_task_id_from_query(query) -> str:
    return query.data.split('/')[1]


async def get_tx_data_by_task_id(
        task_id: str,
        redis_conn: Redis
) -> dict:
    byte_data = await redis_conn.hget('tasks', task_id)
    await redis_conn.hdel('tasks', task_id)

    if not byte_data:
        raise RedisTaskNotFoundException('Transaction already rejected or executed!')

    data = json.loads(byte_data)
    return data
