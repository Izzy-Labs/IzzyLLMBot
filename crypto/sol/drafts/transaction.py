import asyncio

from solana.rpc.async_api import AsyncClient


async def main():
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
    print(res)  # True


if __name__ == "__main__":
    asyncio.run(main())
