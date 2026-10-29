from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
import datetime
from decimal import Decimal


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
