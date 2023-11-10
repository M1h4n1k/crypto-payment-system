from bson import ObjectId
from datetime import datetime
import motor.motor_asyncio
import os
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL') or 'mongodb://localhost:27017')
db = client.orders


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


class Order(BaseModel):
    id: Annotated[str, AfterValidator(check_object_id)] = Field(default_factory=lambda: ObjectId().binary.hex(), alias='_id')
    currency: str = Field(default='')
    currencyCrypto: str = Field(default='')
    amountEUR: float = Field(...)
    amountCrypto: float = Field(default=10000)
    description: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: str = Field(default='')
    status: int = Field(default=0)
    address: str = Field(default='')
    stage: int = Field(default=0)
    callback_url: str = Field()
    # Sign to check the integrity of the data. You can calculate it as you wish. E.g. sha256(f'{currency}:{amountEUR}')
    sign: str = Field(...)

    class Config:
        populate_by_name = True


class UpdateOrder(BaseModel):
    id: Annotated[str, AfterValidator(check_object_id)] | None = Field(default=None)
    currencyCrypto: str | None = Field(default=None)
    amountCrypto: float | None = Field(default=None)
    email: str | None = Field(default=None)
    stage: int | None = Field(default=None)

