import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import UUID, DateTime
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
