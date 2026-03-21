from src.application.ports.services import IOrderService
from src.application.ports.uow import IUnitOfWork
from src.config import SERVICE_NAME, Settings
from src.domain.entities import Product
from src.domain.enums import EventType
from src.infrastructure.messaging.messages import ExternalReference, FailedMessage
from src.infrastructure.models import OutboxModel


class OrderServiceProxy(IOrderService):
    def __init__(self, settings: Settings):
        self.topic = settings.SAGA_EVENTS_TOPIC
        self.producer = SERVICE_NAME

    async def products_reserved(
        self, uow: IUnitOfWork, products: list[Product], external_reference: ExternalReference
    ):
        for_outbox = OutboxModel(
            action=EventType.PRODUCTS_RESERVED,
            topic=self.topic,
            payload={
                'products': [product.to_dict() for product in products],
                'total_price': sum(int(product.price) * product.quantity for product in products),
            },
            external_reference=external_reference.to_dict(),
            producer=self.producer,
        )
        await uow.outbox.add(for_outbox)

    async def products_committed(
        self, uow: IUnitOfWork, products: list[Product], external_reference: ExternalReference
    ):
        for_outbox = OutboxModel(
            action=EventType.PRODUCTS_COMMITTED,
            topic=self.topic,
            payload={
                'products': [product.to_dict() for product in products],
            },
            external_reference=external_reference.to_dict(),
            producer=self.producer,
        )
        await uow.outbox.add(for_outbox)

    async def action_failed(self, uow: IUnitOfWork, message: FailedMessage):
        for_outbox = OutboxModel(
            action=message.action,
            topic=self.topic,
            payload=message.payload.to_dict(),
            external_reference=message.external_reference.to_dict(),
            producer=self.producer,
        )
        await uow.outbox.add(for_outbox)
