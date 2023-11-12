import os
import aiohttp


async def format_transactions(transactions: list[dict]) -> list[dict]:
    return [
        {
            'hash': tx['transaction_id']['hash'],
            'confirmations': -1,
            'value': int(tx['in_msg']['value']) / 1000000000,
        } for tx in transactions
    ]


async def get_transactions(address: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            'https://testnet.toncenter.com/api/v2/getTransactions',
            params={
                'address': address,
                'limit': 100,
            },
            headers={
                'Accepts': 'application/json',
                'X-API-Key': os.getenv('TON_API_KEY'),
            }
        )
        data = await resp.json()
        return await format_transactions(data['result'])