import os
import aiohttp


async def filter_unconfirmed():
    pass


async def format_transactions(transactions: list[dict]) -> list[dict]:
    return [
        {
            'hash': tx['tx_hash'],
            'confirmations': tx['confirmations'],
            'value': tx['value'] / 100000000,
        } for tx in transactions
    ]


async def get_transactions(address: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            f'https://api.blockcypher.com/v1/btc/test3/addrs/{address}',
            headers={
                'Accepts': 'application/json',
            },
            params={
                'token': os.getenv('BTC_API_KEY'),
            }
        )
        data = await resp.json()
        return await format_transactions(data['txrefs'])
