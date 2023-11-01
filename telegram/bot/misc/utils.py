import json
import requests

from aioredis import Redis
from psycopg2 import connect
from solders.pubkey import Pubkey

from .exceptions import RedisTaskNotFoundException


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
    base_link = 'https://api.dexscreener.com/latest/dex/search?q='

    response = requests.get(
        base_link + token_name,
    ).json()

    for pair in response['pairs']:
        if pair['chainId'] == 'solana':
            return pair['quoteToken']['address']

    raise ValueError(f'token {token_name} not found')


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
