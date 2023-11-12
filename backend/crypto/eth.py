import os
import aiohttp


async def filter_unconfirmed():
    pass


async def format_transactions(transactions: list[dict]) -> list[dict]:
    return [
        {
            'hash': tx['hash'],
            'confirmations': int(tx['confirmations']),
            'value': int(tx['value']) / 1000000000000000000,
        } for tx in transactions
    ]


async def get_transactions(address: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            'https://api-sepolia.etherscan.io/api',
            params={
                'module': 'account',
                'action': 'txlist',
                'address': address,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'asc',
                'apikey': os.getenv('ETH_API_KEY'),
            },
            headers={
                'Accepts': 'application/json',
            }
        )
        data = await resp.json()
        return await format_transactions(data['result'])