from src.application.ports.repositories import (
    IOutboxRepository,
    IProcessedMessagesModelRepository,
    IProductRepository,
    IStockRepository,
)
from src.application.ports.uow import IUnitOfWork
from src.infrastructure.repositories.outbox_repository import OutboxRepository
from src.infrastructure.repositories.processed_message_repository import (
    ProcessedMessagesModelRepository,
)
from src.infrastructure.repositories.product_repository import ProductRepository
from src.infrastructure.repositories.stock_repository import StockRepository
from src.infrastructure.session import async_session


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self.__session_factory = session_factory

    async def __aenter__(self):
        self.__session = self.__session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self.rollback()
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    @property
    def outbox(self) -> IOutboxRepository:
        return OutboxRepository(self.__session)

    @property
    def processed_messages(self) -> IProcessedMessagesModelRepository:
        return ProcessedMessagesModelRepository(self.__session)

    @property
    def stocks(self) -> IStockRepository:
        return StockRepository(self.__session)

    @property
    def products(self) -> IProductRepository:
        return ProductRepository(self.__session)


def get_uow() -> IUnitOfWork:
    return UnitOfWork(session_factory=async_session)
