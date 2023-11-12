from .currencies import CURRENCIES
from .btc import get_transactions as get_btc
from .eth import get_transactions as get_eth
from .ton import get_transactions as get_ton


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


__all__ = ['CURRENCIES', 'check_paid']