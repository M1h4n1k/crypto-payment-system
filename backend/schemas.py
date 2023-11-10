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


class OrderIn(BaseModel):
    """
    Attributes:
        currency: Currency name
        amountFiat: Amount in fiat currency, actually not only fiat but any currency u want, but mainly fiat is easier
        description: Description of the payment. Not used anywhere on client side
        email: Payer's email if u can set that
        callback_url: Server url to notify on successful payment
        sign: Sign to check the integrity of the data. You can calculate it as you wish. E.g. sha256(f'{currency}:{amountEUR}')
    """
    currency: str = Field()
    amountFiat: float = Field()
    description: str = Field(default='')
    email: str = Field(default='')
    callback_url: str = Field()
    sign: str = Field()


class Order(OrderIn):
    """
    Attributes:
        id: Order id in mongodb
        currencyCrypto: Crypto currency name
        amountCrypto: Amount in cryptocurrency
        created_at: Creation date
        status: Status paid/unpaid (0/1)
        address: Address which will receive the money
        stage: Stage user stage while paying (0/1/2)
    """
    id: Annotated[str, AfterValidator(check_object_id)] = Field(default_factory=lambda: ObjectId().binary.hex(), alias='_id')
    currencyCrypto: str = Field(default='')
    amountCrypto: float = Field(default=-1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=0)
    address: str = Field(default='')
    stage: int = Field(default=0)

    class Config:
        populate_by_name = True


class OrderUpdIn(BaseModel):
    currencyCrypto: str | None = Field(default=None)
    email: str | None = Field(default=None)
    stage: int | None = Field(default=None)


class OrderUpd(OrderUpdIn):
    id: Annotated[str, AfterValidator(check_object_id)] | None = Field(default=None)
    amountCrypto: float | None = Field(default=None)
    address: str | None = Field(default=None)


