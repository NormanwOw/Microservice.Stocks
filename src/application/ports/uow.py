from abc import ABC, abstractmethod

from src.application.ports import repositories as i


class IUnitOfWork(ABC):
    outbox: i.IOutboxRepository
    processed_messages: i.IProcessedMessagesModelRepository
    products: i.IProductRepository
    stocks: i.IStockRepository

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
