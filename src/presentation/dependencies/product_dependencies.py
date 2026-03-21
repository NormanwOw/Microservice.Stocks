from src.application.use_cases.add_products_use_case import AddProducts
from src.application.use_cases.cancel_reserve_use_case import CancelReserveProducts
from src.application.use_cases.commit_products_use_case import CommitProducts
from src.application.use_cases.get_products_use_case import GetProducts
from src.application.use_cases.reserve_products_use_case import (
    ReserveProducts,
)
from src.config import settings
from src.infrastructure.logger.impl import logger
from src.infrastructure.services.order_service_proxy import OrderServiceProxy
from src.infrastructure.uow.impl import get_uow


class ProductDependencies:
    order_service_proxy = OrderServiceProxy(settings)

    @classmethod
    async def get_products(cls):
        return GetProducts(get_uow())

    @classmethod
    async def add_products(cls):
        return AddProducts(get_uow())

    @classmethod
    async def reserve_products(cls):
        return ReserveProducts(cls.order_service_proxy, logger)

    @classmethod
    async def commit_products(cls):
        return CommitProducts(cls.order_service_proxy, logger)

    @classmethod
    async def cancel_reserve(cls):
        return CancelReserveProducts()
