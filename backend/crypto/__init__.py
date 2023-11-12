from .currencies import CURRENCIES
from .btc import get_transactions as get_btc
from .eth import get_transactions as get_eth
from .ton import get_transactions as get_ton
import os
import aiohttp


async def check_paid(address: str, currency: str, amount: float, get_transaction) -> bool | dict:
    transactions = []
    if currency == 'TON':
        transactions = await get_ton(address)
    elif currency == 'ETH':
        transactions = await get_eth(address)
    elif currency == 'BTC':
        transactions = await get_btc(address)

    for tx in transactions:
        if await get_transaction(tx['hash'], currency) is not None:
            continue
        if tx['confirmations'] < CURRENCIES[currency]['confirmations'] and CURRENCIES[currency]['confirmations'] != -1:
            continue
        if abs(tx['value'] - amount) < 0.00000001:
            return tx
    return False


async def get_price(symbol: str, fiat: str) -> float:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            'https://pro-api.coinmarketcap.com/v2/tools/price-conversion',
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY'),
            },
            params={
                'amount': 1,
                'symbol': fiat,
                'convert_id': CURRENCIES[symbol]['cmc_id'],
            }
        )
        data = await resp.json()
        return data['data'][0]['quote'][CURRENCIES[symbol]['cmc_id']]['price']


__all__ = ['CURRENCIES', 'check_paid', 'get_price']