import os
import aiohttp
import schemas
from crud import get_transaction, create_transaction


async def get_ton_transactions(address: str) -> list[dict]:
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
        return data['result']


async def get_eth_transactions(address: str) -> list[dict]:
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
        return data['result']


async def check_paid(order: schemas.Order) -> bool:
    if order.currencyCrypto == 'TON':
        transactions = await get_ton_transactions(order.address)
        for transaction in transactions:
            if await get_transaction(transaction['transaction_id']['hash'], order.currencyCrypto) is not None:
                continue
            if abs(int(transaction['in_msg']['value']) / 1000000000 - order.amountCrypto) < 0.000001:
                tx = schemas.Transaction(
                    txid=transaction['transaction_id']['hash'],
                    currency=order.currencyCrypto,
                )
                await create_transaction(tx)
                return True
    if order.currencyCrypto == 'ETH':
        transactions = await get_eth_transactions(order.address)
        for transaction in transactions:
            if transaction['isError'] != '0' or int(transaction['confirmations']) < 12:
                continue
            if await get_transaction(transaction['hash'], order.currencyCrypto) is not None:
                continue
            if abs(int(transaction['value']) / 1000000000000000000 - order.amountCrypto) < 0.000001:
                tx = schemas.Transaction(
                    txid=transaction['hash'],
                    currency=order.currencyCrypto,
                )
                await create_transaction(tx)
                return True
    return False
