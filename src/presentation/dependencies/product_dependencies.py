from src.application.use_cases.get_products_use_case import GetProducts
from src.application.use_cases.reserve_products_use_case import (
    ReserveProducts,
)
from src.infrastructure.logger.impl import logger
from src.infrastructure.uow.impl import get_uow


class ProductDependencies:
    @classmethod
    async def get_products(cls):
        return GetProducts(get_uow())

    @classmethod
    async def reserve_products(cls):
        return ReserveProducts(logger)
