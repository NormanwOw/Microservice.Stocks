from decimal import Decimal
from uuid import UUID

from pydantic import Field

from src.domain.base import PydanticBase
from src.domain.enums import Currency


class Product(PydanticBase):
    id: UUID
    name: str
    quantity: int
    price: Decimal = Field(examples=[Decimal('10.00')])
    currency: Currency = Currency.USD
