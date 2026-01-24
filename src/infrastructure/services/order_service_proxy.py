from src.config import Settings
from src.domain.entities import Product
from src.domain.enums import EventType
from src.infrastructure.messaging.messages import ExternalReference
from src.infrastructure.models import OutboxModel
from src.infrastructure.services.interfaces import IOrderService
from src.infrastructure.uow.interfaces import IUnitOfWork


class OrderServiceProxy(IOrderService):
    def __init__(self, settings: Settings):
        self.topic = settings.SAGA_EVENTS_TOPIC
        self.producer = 'stocks-service'

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

    async def reserve_failed(
        self, uow: IUnitOfWork, error_message: str, external_reference: ExternalReference
    ):
        for_outbox = OutboxModel(
            action=EventType.RESERVE_FAILED,
            topic=self.topic,
            payload={'error_message': error_message},
            external_reference=external_reference.to_dict(),
            producer=self.producer,
        )
        await uow.outbox.add(for_outbox)
