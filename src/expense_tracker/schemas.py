import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    description: str = Field(min_length=1, max_length=200)
    date: datetime.date
    category_id: int


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    description: str
    date: datetime.date
    category_id: int


class BudgetUpsert(BaseModel):
    category_id: int
    month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    limit_amount: Decimal = Field(ge=0, max_digits=12, decimal_places=2)


class BudgetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    month: str
    limit_amount: Decimal


class BudgetStatus(BaseModel):
    category_id: int
    category_name: str
    month: str
    limit_amount: Decimal
    spent: Decimal
    remaining: Decimal
    exceeded: bool
