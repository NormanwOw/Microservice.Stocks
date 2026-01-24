from abc import ABC, abstractmethod


class IOrderService(ABC):
    @abstractmethod
    async def products_reserved(self):
        raise NotImplementedError

    @abstractmethod
    async def reserve_failed(self):
        raise NotImplementedError
