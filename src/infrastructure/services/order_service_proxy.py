from src.config import Settings
from src.infrastructure.models import OutboxModel
from src.infrastructure.services.interfaces import IOrderService
from src.infrastructure.uow.interfaces import IUnitOfWork


class OrderServiceProxy(IOrderService):
    def __init__(self, uow: IUnitOfWork, settings: Settings):
        self.uow = uow
        self.topic = settings.SAGA_EVENTS_TOPIC

    async def products_reserved(self):
        for_outbox = OutboxModel()
        await self.uow.outbox.add(for_outbox)

    async def reserve_failed(self):
        for_outbox = OutboxModel()
        await self.uow.outbox.add(for_outbox)
