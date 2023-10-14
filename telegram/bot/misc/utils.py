import requests

from psycopg2 import connect
from solders.pubkey import Pubkey


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
