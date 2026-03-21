from abc import ABC, abstractmethod

from src.application.ports.uow import IUnitOfWork
from src.domain.entities import Product
from src.infrastructure.messaging.messages import ExternalReference, FailedMessage


class IOrderService(ABC):
    @abstractmethod
    async def products_reserved(
        self, uow: IUnitOfWork, products: list[Product], external_reference: ExternalReference
    ):
        raise NotImplementedError

    @abstractmethod
    async def products_committed(
        self, uow: IUnitOfWork, products: list[Product], external_reference: ExternalReference
    ):
        raise NotImplementedError

    @abstractmethod
    async def action_failed(self, uow: IUnitOfWork, message: FailedMessage):
        raise NotImplementedError
