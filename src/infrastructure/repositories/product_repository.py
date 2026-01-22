from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import ProductsModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IProductRepository


class ProductRepository(SQLAlchemyRepository, IProductRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, ProductsModel)
