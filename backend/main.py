from fastapi import Depends, FastAPI, Response, Cookie
from starlette.middleware.cors import CORSMiddleware
import crud
import schemas
import aiohttp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

CURRENCIES = {
    'BTC': {
        'cmc_id': '1',
        'color': '#F7931A',
    },
    'ETH': {
        'cmc_id': '1027',
        'color': '#627EEA',
    },
    'USDT': {
        'cmc_id': '825',
        'color': '#26A17B',
    },
    'TON': {
        'cmc_id': '11419',
        'color': '#0088CC',
    },
}


async def get_crypto_price(symbol: str) -> float:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            'https://pro-api.coinmarketcap.com/v2/tools/price-conversion',
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY'),
            },
            params={
                'amount': 1,
                'symbol': 'USD',
                'convert_id': CURRENCIES[symbol]['cmc_id'],
            }
        )
        data = await resp.json()
        return data['data'][0]['quote'][CURRENCIES[symbol]['cmc_id']]['price']


@app.get('/order/{_id}')
async def get_order(_id: str):
    order = await crud.get_order(_id)
    if order is None:
        return Response(status_code=404)
    return order


@app.post('/order')
async def create_order(order: schemas.Order):
    return await crud.create_order(order)


@app.put('/order/{_id}')
async def update_order(_id: str, order: schemas.UpdateOrder):
    upd_order = await crud.get_order(_id)
    if upd_order is None:
        return Response(status_code=404)

    order.id = _id
    if CURRENCIES.get(order.currencyCrypto) is not None:
        ratio = await get_crypto_price(order.currencyCrypto)
        order.amountCrypto = upd_order.amountEUR * ratio

    return await crud.update_order(order)


@app.get('/currencies')
async def get_currencies():
    return CURRENCIES
