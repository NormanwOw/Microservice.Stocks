from decimal import Decimal

from pydantic import BaseModel, Field

from src.domain.enums import Currency


class AddProductSchema(BaseModel):
    name: str
    quantity: int
    price: Decimal = Field(examples=[Decimal('10.00')])
    currency: Currency = Currency.USD
