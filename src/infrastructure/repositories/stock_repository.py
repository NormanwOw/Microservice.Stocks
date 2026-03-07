from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.repositories import IStockRepository
from src.domain.entities import Product
from src.infrastructure.models import StocksModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.presentation.pagination import Pagination


class StockRepository(SQLAlchemyRepository, IStockRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, StocksModel)

    async def find(self, pagination: Pagination) -> list[StocksModel]:
        query = await self.__session.scalars(
            select(StocksModel)
            .where(StocksModel.available > 0)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        return list(query.all())

    async def find_available(
        self, products: list[Product], with_for_update: bool = False
    ) -> list[StocksModel]:
        stmt = select(StocksModel).where(
            StocksModel.product_id.in_([product.id for product in products]),
            StocksModel.available > 0,
        )
        if with_for_update:
            stmt = stmt.with_for_update()

        res = await self.__session.scalars(stmt)
        return list(res.all())

    async def find_total(
        self, products: list[Product], with_for_update: bool = False
    ) -> list[StocksModel]:
        stmt = select(StocksModel).where(
            StocksModel.product_id.in_([product.id for product in products]),
            StocksModel.total > 0,
        )
        if with_for_update:
            stmt = stmt.with_for_update()

        res = await self.__session.scalars(stmt)
        return list(res.all())
