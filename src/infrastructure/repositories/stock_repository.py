from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import StocksModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IStockRepository


class StockRepository(SQLAlchemyRepository, IStockRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, StocksModel)
