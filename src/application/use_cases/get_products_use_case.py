from src.domain.entities import Product
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.pagination import Pagination


class GetProducts:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, pagination: Pagination) -> list[Product]:
        async with self.uow:
            stocks = await self.uow.stocks.find_available(pagination=pagination)
            return [stock.to_product() for stock in stocks]
