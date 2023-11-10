from fastapi import Depends, FastAPI, Response, Cookie
from starlette.middleware.cors import CORSMiddleware
import crud
import schemas
import aiohttp
import os
from config import CURRENCIES


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


async def get_crypto_price(symbol: str, fiat: str) -> float:
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


async def check_paid(order: schemas.Order) -> bool:
    if order.currencyCrypto == 'TON':
        transactions = await get_ton_transactions(order.address)
        for transaction in transactions:
            if abs(int(transaction['in_msg']['value']) / 1000000000 - order.amountCrypto) < 0.000001:
                return True
    return False


async def notify(order: schemas.Order):
    async with aiohttp.ClientSession() as session:
        try:
            await session.post(
                order.callback_url,
                json=order.model_dump(mode='json'),
                headers={
                    'User-agent': 'Payments notifier 1.0.0',
                }
            )
        finally:
            pass


@app.get('/order/{_id}')
async def get_order(_id: str):
    order = await crud.get_order(_id)
    if order is None:
        return Response(status_code=404)
    if order.status == 1:
        return order

    if order.stage == 2 and await check_paid(order):
        order.status = 1
        await crud.update_order(order)
        await notify(order)

    return order


@app.post('/order')
async def create_order(order: schemas.OrderIn):
    return await crud.create_order(schemas.Order(**order.model_dump()))


@app.put('/order/{_id}')
async def update_order(_id: str, order: schemas.OrderUpdIn):
    full_order = await crud.get_order(_id)
    if full_order is None:
        return Response(status_code=404)

    order = schemas.OrderUpd(**order.model_dump())
    order.id = _id
    if CURRENCIES.get(order.currencyCrypto) is not None:
        ratio = await get_crypto_price(order.currencyCrypto, full_order.currency)
        order.amountCrypto = full_order.amountFiat * ratio
        order.address = CURRENCIES[order.currencyCrypto].get('address')

    return await crud.update_order(order)


@app.get('/currencies')
async def get_currencies():
    return CURRENCIES
