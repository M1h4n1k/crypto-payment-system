from fastapi import Depends, FastAPI, Response, Cookie
from starlette.middleware.cors import CORSMiddleware
import crud
import schemas


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
        'color': '#F7931A',
    },
    'ETH': {
        'color': '#627EEA',
    },
    'USDT': {
        'color': '#26A17B'
    },
    'BNB': {
        'color': '#F3BA2F',
    },
    'TON': {
        'color': '#0088CC',
    },
    'TRON': {
        'color': '#D9012C',
    }
}


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
        ratio = 5  # recalculate ratio
        order.amountCrypto = upd_order.amountEUR * ratio

    return await crud.update_order(order)


@app.get('/currencies')
async def get_currencies():
    return CURRENCIES