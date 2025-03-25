from pydantic import BaseModel, PositiveInt
from datetime import date


class SpendingScheme(BaseModel):
    name: str
    date: date
    money: float


class CreateSpending(SpendingScheme):
    user_id: PositiveInt


class ReturnSpendingScheme(SpendingScheme):
    id: PositiveInt
    user_id: PositiveInt


class XLSSpendingScheme(BaseModel):
    id: PositiveInt
    name: str
    date: date
    money: float
