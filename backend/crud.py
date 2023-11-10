from datetime import datetime
from fastapi.encoders import jsonable_encoder
import schemas
from schemas import db


async def create_order(order: schemas.Order) -> schemas.Order:
    order.status = 0
    order.created_at = datetime.utcnow()
    order.stage = 0
    new_order = await db['orders'].insert_one(jsonable_encoder(order))
    created_order = await db['orders'].find_one({'_id': new_order.inserted_id})
    return created_order


async def get_order(_id: str) -> schemas.Order | None:
    order = await db['orders'].find_one({'_id': _id})
    if order is None:
        return None
    return schemas.Order.model_validate(order)


async def update_order(order: schemas.UpdateOrder) -> schemas.Order:
    await db['orders'].update_one({'_id': order.id}, {'$set': order.model_dump(exclude_none=True, exclude={'id'})})
    updated_order = await db['orders'].find_one({'_id': order.id})
    return updated_order

