from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import StocksModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IStockRepository
from src.presentation.pagination import Pagination


class StockRepository(SQLAlchemyRepository, IStockRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, StocksModel)

    async def find_available(self, pagination: Pagination) -> list[StocksModel]:
        query = await self.__session.scalars(
            select(StocksModel)
            .where(StocksModel.available > 0)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        return list(query.all())
