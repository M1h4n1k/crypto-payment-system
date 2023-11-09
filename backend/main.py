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


@app.get('/order/{_id}')
async def get_order(_id: str):
    return await crud.get_order(_id)


@app.post('/order')
async def create_order(order: schemas.Order):
    return await crud.create_order(order)


@app.put('/order/{_id}')
async def update_order(_id: str, order: schemas.UpdateOrder):
    upd_order = await crud.get_order(_id)
    if upd_order is None:
        return Response(status_code=404)

    if order.email is not None:
        upd_order.email = order.email
    if order.currencyCrypto is not None:
        upd_order.currencyCrypto = order.currencyCrypto
        ratio = 3  # recalculate ratio
        upd_order.amountCrypto = upd_order.amountEUR * ratio
    if order.stage is not None:
        upd_order.stage = order.stage

    return await crud.update_order(upd_order)


@app.get('/currencies')
async def get_currencies():
    return {
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