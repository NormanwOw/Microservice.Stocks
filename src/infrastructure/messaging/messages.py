from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.base import PydanticBase
from src.domain.entities import Product
from src.domain.enums import AggregateType, CommandType, EventType


class Message(PydanticBase):
    message_id: UUID = Field(default_factory=uuid4)
    producer: str
    sent_at: datetime | None = None


class ExternalReference(PydanticBase):
    id: UUID
    type: AggregateType
    version: int


class EventMessage(Message):
    action: EventType
    external_reference: ExternalReference


class CommandMessage(Message):
    action: CommandType
    external_reference: ExternalReference


class ReserveProductsPayload(PydanticBase):
    products: list[Product]


class ReserveProductsMessage(CommandMessage):
    payload: ReserveProductsPayload
