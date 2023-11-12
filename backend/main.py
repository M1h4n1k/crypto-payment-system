from fastapi import Depends, FastAPI, Response, Cookie
from starlette.middleware.cors import CORSMiddleware
import crud
import schemas
import aiohttp
import os
from config import CURRENCIES
import re
from crypto_checking import check_paid


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


email_regex = re.compile(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')


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

    if order.email is not None and not re.match(email_regex, order.email):
        return Response(status_code=400, content='Invalid email')

    order = schemas.OrderUpd(**order.model_dump())
    order.id = _id
    if CURRENCIES.get(order.currencyCrypto) is not None:
        ratio = await get_crypto_price(order.currencyCrypto, full_order.currency)
        order.amountCrypto = round(full_order.amountFiat * ratio, 8)
        order.address = CURRENCIES[order.currencyCrypto].get('address')

    return await crud.update_order(order)


@app.get('/currencies')
async def get_currencies():
    return CURRENCIES
