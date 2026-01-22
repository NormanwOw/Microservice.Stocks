import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlalchemy import UUID, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.domain.entities import Product
from src.domain.enums import Currency


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, nullable=False, primary_key=True, default=uuid.uuid4
    )


class CUModel:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc)
    )


class ProductsModel(Base, CUModel):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency, name='currency_enum', native_enum=True, create_type=True),
        nullable=False,
        default=Currency.USD,
    )
    stock: Mapped['StocksModel'] = relationship(
        back_populates='product',
        lazy='selectin',
        uselist=False,
    )


class StocksModel(Base, CUModel):
    __tablename__ = 'stocks'

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True
    )
    available: Mapped[int] = mapped_column(nullable=False, default=0, index=True)
    reserved: Mapped[int] = mapped_column(nullable=False, default=0)
    total: Mapped[int] = mapped_column(nullable=False, default=0)

    product: Mapped['ProductsModel'] = relationship(
        back_populates='stock',
        lazy='selectin',
        uselist=False,
    )

    def to_product(self) -> Product:
        return Product(
            id=self.product.id,
            name=self.product.name,
            quantity=self.available,
            price=self.product.price,
            currency=self.product.currency,
        )


class OutboxModel(Base, CUModel):
    __tablename__ = 'outbox'

    action: Mapped[str] = mapped_column(nullable=False)
    topic: Mapped[str] = mapped_column(nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    external_reference: Mapped[dict] = mapped_column(JSONB, nullable=False)
    producer: Mapped[str] = mapped_column(nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )


class ProcessedMessagesModel(Base, CUModel):
    __tablename__ = 'processed_messages'
