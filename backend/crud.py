from datetime import datetime
from fastapi.encoders import jsonable_encoder
import schemas
from schemas import db


async def create_order(order: schemas.Order) -> schemas.Order:
    new_order = await db['orders'].insert_one(jsonable_encoder(order))
    created_order = await db['orders'].find_one({'_id': new_order.inserted_id})
    return created_order


async def get_order(_id: str) -> schemas.Order | None:
    order = await db['orders'].find_one({'_id': _id})
    if order is None:
        return None
    return schemas.Order.model_validate(order)


async def update_order(order: schemas.OrderUpd | schemas.Order) -> schemas.Order:
    await db['orders'].update_one({'_id': order.id}, {'$set': order.model_dump(exclude_none=True, exclude={'id'})})
    updated_order = await db['orders'].find_one({'_id': order.id})
    return updated_order


async def get_transaction(txid: str, currency: str) -> schemas.Transaction | None:
    transaction = await db['transactions'].find_one({'txid': txid, 'currency': currency})
    if transaction is None:
        return None
    return schemas.Transaction.model_validate(transaction)


async def create_transaction(transaction: schemas.Transaction) -> schemas.Transaction:
    new_transaction = await db['transactions'].insert_one(jsonable_encoder(transaction))
    created_transaction = await db['transactions'].find_one({'_id': new_transaction.inserted_id})
    return created_transaction

