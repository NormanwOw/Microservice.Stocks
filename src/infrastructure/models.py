import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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

    name: Mapped[str] = mapped_column(nullable=False)


class StocksModel(Base, CUModel):
    __tablename__ = 'stocks'

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'), nullable=False
    )
    available: Mapped[int] = mapped_column(nullable=False, default=0)
    reserved: Mapped[int] = mapped_column(nullable=False, default=0)
    total: Mapped[int] = mapped_column(nullable=False, default=0)


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
