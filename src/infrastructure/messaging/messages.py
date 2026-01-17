from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    message_id: UUID = Field(default_factory=uuid4)


class EventMessage(Message):
    event_type: str
